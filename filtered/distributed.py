from distributask.distributask import create_from_config
from .filter import read_json_in_batches
from .worker import run_job
from tqdm import tqdm
import time

if __name__ == "__main__":

    input_filename = "datasets/cap3d_captions.json"
    batch_size = 10000

    distributask = create_from_config()

    max_price = 0.25
    max_nodes = 25
    docker_image = "antbaez/filter-worker:latest"
    module_name = "filtered.worker"

    redis_client = distributask.get_redis_connection()

    rented_nodes = distributask.rent_nodes(
        max_price, max_nodes, docker_image, module_name
    )
    print("Total nodes rented: ", len(rented_nodes))

    distributask.register_function(run_job)

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

        print(total_batches)
        task = distributask.execute_function(
            "run_job", {"batch_index": total_batches, "batch": batch}
        )

        tasks.append(task)

    first_task_done = False
    print("Tasks sent. Starting monitoring")

    inactivity_log = {node["instance_id"]: 0 for node in rented_nodes}

    start_time = time.time()
    with tqdm(total=len(tasks), unit="task") as pbar:
        while not all(task.ready() for task in tasks):

            current_tasks = sum([task.ready() for task in tasks])
            pbar.update(current_tasks - pbar.n)

            time.sleep(1)

            current_time = time.time()
            if current_time - start_time > 60:
                start_time = time.time()

                for node in rented_nodes:
                    log_response = distributask.get_node_log(node)
                    if log_response.status_code == 200:
                        try:
                            last_msg = log_response.text.splitlines()[-1]
                            if ("Task complete" in last_msg and inactivity_log[node["instance_id"]] == 0):
                                inactivity_log[node["instance_id"]] = 1
                            elif ("Task complete" in last_msg and inactivity_log[node["instance_id"]] == 1):
                                distributask.terminate_nodes([node])
                                print("node terminated")
                            else:
                                inactivity_log[node["instance_id"]] == 0
                        except:
                            pass
