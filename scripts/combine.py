import os
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_valid_content(content):
    # Check if the content matches the expected format
    return content.strip().startswith(',') or content.strip().startswith('{')

def parse_content(content):
    # Remove leading comma if present
    if content.strip().startswith(','):
        content = content[1:].strip()
    
    # Wrap in curly braces if not already present
    if not content.strip().startswith('{'):
        content = '{' + content + '}'
    
    return json.loads(content)

def combine_files(directory):
    combined_data = {}
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            logging.info(f"Processing file: {filename}")
            
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    if is_valid_content(content):
                        data = parse_content(content)
                        combined_data.update(data)
                        logging.info(f"Successfully parsed and added data from {filename}")
                    else:
                        logging.warning(f"Skipping file {filename} - content doesn't match expected format")
            except Exception as e:
                logging.error(f"Error processing file {filename}: {e}")

    logging.info(f"Total number of key-value pairs in combined data: {len(combined_data)}")
    return combined_data

# Specify the directory containing the files
directory = './filtered_files'  # Adjust this path if needed

# Combine the files
result = combine_files(directory)

if result:
    output_file = './filtered/cap3d_captions.json'
    try:
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=4)
        logging.info(f"Combined data has been written to {output_file}")
    except IOError as e:
        logging.error(f"Error writing to output file: {e}")
else:
    logging.warning("No data was combined. The output file was not created.")

print("Script execution completed. Please check the logs for details.")