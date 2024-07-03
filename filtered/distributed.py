
from distributaur.distributaur import create_from_config
from .filter import read_json_in_batches
from .worker import run_job
from tqdm import tqdm
import time


if __name__ == "__main__":

    input_filename = 'datasets/cap3d_captions.json'
    batch_size = 1000

    distributaur = create_from_config()

    max_price = 0.1
    max_nodes = 50
    docker_image = "antbaez/filter-worker:latest"
    module_name = "filtered.worker"

    redis_client = distributaur.get_redis_connection()

    rented_nodes = distributaur.rent_nodes(max_price, max_nodes, docker_image, module_name)
    print("Total nodes rented: ", len(rented_nodes))

    distributaur.register_function(run_job)

    while True:
        user_input = input("press r when workers are ready: ")
        if user_input == "r":
            break


    total_batches = 0
    
    print("Sending tasks")
    tasks = []

    json_batches = [batch for batch in read_json_in_batches(input_filename, batch_size)]
    print(f"number of batches: {len(json_batches)}")

    num_batches = len(json_batches)
    for i in range(num_batches):

        batch = json_batches[i]

        total_batches += 1
        task = distributaur.execute_function("run_job", {
            "batch_index" : total_batches,
            "batch" : batch
        })

        tasks.append(task)

    first_task_done = False
    print("Tasks sent. Starting monitoring")
    with tqdm(total=len(tasks), unit="task") as pbar:
        while not all(task.ready() for task in tasks):
            current_tasks = sum([task.ready() for task in tasks])
            pbar.update(current_tasks - pbar.n)
            if current_tasks > 0:
                if not first_task_done:
                    first_task_done = True
                    first_task_start_time = time.time()

                end_time = time.time()
                elapsed_time = end_time - first_task_start_time
                time_per_tasks = elapsed_time / current_tasks
                time_left = time_per_tasks * (len(tasks) - current_tasks)

                pbar.set_postfix(
                    elapsed=f"{elapsed_time:.2f}s", time_left=f"{time_left:.2f}"
                )
            time.sleep(2)
