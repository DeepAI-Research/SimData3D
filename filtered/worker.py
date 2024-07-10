import sys
from .filter import filter_captions, write_filtered_json

def run_job(batch_index, batch):

    if len(str(batch_index)) == 1:
        batch_num = f"0{batch_index}"
    else:
        batch_num = f"{batch_index}"

    output_filename = f"batch_{batch_num}"

    filtered_batch = filter_captions(batch)
    write_filtered_json(output_filename, filtered_batch)

    distributask.upload_file(output_filename)

    return "Task complete"


if __name__ == "__main__" or any("celery" in arg for arg in sys.argv):
    from distributask.distributask import create_from_config

    distributask = create_from_config()
    distributask.register_function(run_job)

    celery = distributask.app