import json
import os
import math

def split_json(input_file, num_files, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Load the input JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    items = list(data.items())
    total_items = len(items)
    chunk_size = math.ceil(total_items / num_files)
    
    for i in range(num_files):
        start_index = i * chunk_size
        end_index = start_index + chunk_size
        chunk_data = dict(items[start_index:end_index])
        output_file_path = os.path.join(output_folder, f'data_{i + 1}.json')
        
        # Save the chunk to a new JSON file
        with open(output_file_path, 'w') as f:
            json.dump(chunk_data, f, indent=4)


if __name__ == '__main__':
    # Example usage
    input_file_path = '../datasets/cap3d_captions.json'
    output_folder = 'prepare'

    num_files = int(input("Enter the number of files to split the data into (will be saved in prepare folder): "))
    
    split_json(input_file_path, num_files, output_folder)
