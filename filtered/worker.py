import sys
from .filter import filter_captions, write_filtered_json


def run_job(batch_index, batch):

    output_filename = f"batch_{batch_index}"

    filtered_batch = filter_captions(batch)
    write_filtered_json(output_filename, filtered_batch)

    distributaur.upload_file(output_filename)

    return "Task complete"


if __name__ == "__main__" or any("celery" in arg for arg in sys.argv):
    from distributaur.distributaur import create_from_config

    distributaur = create_from_config()
    distributaur.register_function(run_job)

    celery = distributaur.app
