import json
import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def count_objects(caption):
    doc = nlp(caption)
    objects = [chunk.text for chunk in doc.noun_chunks]
    print("These are the objects:", objects)
    return len(objects)

def read_json_in_batches(filename, batch_size=100):
    with open(filename, 'r') as file:
        data = json.load(file)
        keys = list(data.keys())
        for i in range(0, len(keys), batch_size):
            yield {k: data[k] for k in keys[i:i+batch_size]}

def filter_captions(data, max_objects=3):
    filtered_data = {}
    for key, caption in data.items():
        if count_objects(caption) <= max_objects:
            filtered_data[key] = caption
    return filtered_data

def write_filtered_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def test_caption_filtering():
    test_data = {
        "ed51a51909ee46c780db3a85e821feb2": "A green and white rifle.",
        "9110b606f6c547b2980fcb3c8c4b6a1c": "a small building with a roof, accompanied by brown and black shelves, a wooden bench, and a brown box.",
        "80d9caaa1fa04502af666135196456e1": "a pair of purple and black swords with white handles.",
        "28d43a218cd8466a8c1f82b29b71e314": "a small house, island, road with trash, trash pile, boat with trash, ship, boat with a man, and a fish in trash."
    }
    # Count number of objects in each caption
    for key, caption in test_data.items():
        print(key, count_objects(caption))

def main():
    # Uncomment the line below to run the test function
    # test_caption_filtering()
    input_filename = '../datasets/cap3d_captions.json'  # Adjusted path
    output_filename = '../filtered/filtered_cap3d_captions.json'  # Adjusted path
    batch_size = 100

    filtered_data = {}
    for batch in read_json_in_batches(input_filename, batch_size):
        filtered_data.update(filter_captions(batch))

    write_filtered_json(output_filename, filtered_data)

if __name__ == '__main__':
    main()
