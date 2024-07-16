import json
from gliner import GLiNER


class Cap3DObjectDetector:
    def __init__(self, model_name="urchade/gliner_medium-v2.1"):
        self.model = GLiNER.from_pretrained(model_name)
        # We'll use a broad set of labels to capture as many objects as possible
        self.labels = ["OBJECT", "PRODUCT", "WORK_OF_ART", "PERSON", "LOCATION", "ORGANIZATION", "EVENT", "ANIMAL", "PLANT", "VEHICLE", "BUILDING", "FURNITURE"]

    def detect_objects(self, caption):
        entities = self.model.predict_entities(caption, self.labels, threshold=0.3)  # Lower threshold for more permissive detection
        
        # Consider all detected entities as potential objects
        objects = [entity["text"] for entity in entities]
        
        # If GLiNER doesn't detect any objects, fall back to simple noun phrase extraction
        if not objects:
            objects = self._extract_noun_phrases(caption)
        
        print("These are the objects:", objects)
        return objects

    def _extract_noun_phrases(self, text):
        # Simple rule-based noun phrase extraction
        words = text.replace(',', '').replace('.', '').split()
        noun_phrases = []
        current_phrase = []
        for word in words:
            if word.lower() not in ['a', 'an', 'the', 'and']:
                current_phrase.append(word)
            else:
                if current_phrase:
                    noun_phrases.append(' '.join(current_phrase))
                    current_phrase = []
        if current_phrase:
            noun_phrases.append(' '.join(current_phrase))
        return noun_phrases

    def count_objects(self, caption):
        objects = self.detect_objects(caption)
        return len(objects)
    

def read_json_in_batches(filename, batch_size=100):
    with open(filename, 'r') as file:
        data = json.load(file)
        keys = list(data.keys())
        for i in range(0, len(keys), batch_size):
            yield {k: data[k] for k in keys[i:i+batch_size]}


def write_filtered_json(filename, data, first_batch=False, last_batch=False):
    mode = 'w' if first_batch else 'a'
    with open(filename, mode) as file:
        if first_batch:
            file.write('{\n')
        elif not first_batch:
            file.write(',\n')
        
        json_str = json.dumps(data, indent=4)[1:-1]  # Convert to JSON string and strip the enclosing braces
        file.write(json_str)
        
        if last_batch:
            file.write('\n}')


def filter_captions(data, max_objects=2):
    detector = Cap3DObjectDetector()
    filtered_data = {}
    for key, caption in data.items():
        if detector.count_objects(caption) <= max_objects:
            filtered_data[key] = caption
    return filtered_data


def test_caption_filtering():
    detector = Cap3DObjectDetector()
    test_data = {
        "caption1": "Star Wars starships, windmill, airplane, helicopter, and droids.",
        "caption2": "A red car parked on the street.",
        "caption3": "Mountains, trees, and a serene lake in the background.",
        "caption4": "A tabby cat sitting on a wooden windowsill, looking outside.",
        "ed51a51909ee46c780db3a85e821feb2": "A green and white rifle.", 
        "9110b606f6c547b2980fcb3c8c4b6a1c": "a small building with a roof, accompanied by brown and black shelves, a wooden bench, and a brown box.", 
        "80d9caaa1fa04502af666135196456e1": "a pair of purple and black swords with white handles.", 
        "28d43a218cd8466a8c1f82b29b71e314": "a small house, island, road with trash, trash pile, boat with trash, ship, boat with a man, and a fish in trash.", 
        "75582285fab442a2ba31733f9c8fae66": "a small, grassy hill.", 
        "53d0b31aa7f84bc4b1733224963d0114": "a white sofa with wooden legs and frame.", 
        "25f25e35aada40e49194657fd51c1199": "a wooden fence with posts and gate, featuring a sand base.", 
        "d7340a5b05b6460facbd90aaafb7f1f1": "a rainbow-colored mountain.", 
        "bb3552fe9b074acf8ea531c2e9e25fe7": "a house with a door, a teal-colored bowl, a room with a blue wall, a curved wall, a pool with sand, a curved wall with a blue door, a wooden boat, and a wooden box.",
        "3764a2442eca43c7bbe64d8297d84905": "A paper clock, brown origami bird, and thin metal clock", 
        "9ff331513cea44a2938d09a03d7b0493": "White plastic cylinder resembling a toilet paper holder.", 
        "f78e38ccea1d45dcaefe1970e7df4035": "a forklift truck with a trailer.", 
        "112c059282cf4511a01fd27211edcae8": "a wooden table and bench.", 
        "77031e12fc7f49c09530addc5c7c1cd3": "A black and white Lego ninja with a bird on his shoulder, holding a sword.", 
        "d06cca5175434a83b3944bcfad47c464": "a small table with stairs, glass top, and shelf in a room.", 
        "037306d9dd4e4a3cbe14d127cfe26fb5": "a small white building with tables, chairs, and a light inside, featuring a lid and beige accents.", "995f110c17cc49b5be4c90ea5028fb1d": "white paper airplane model", 
        "24a550a5d6e54402809a75eb8654230e": "a small brick building with a blue roof and green and white walls.", 
        "1c4cdf7a3b46436daad57548a5587025": "A white pillow with a logo and the words \"picture mind\" on it, accompanied by a curved white wall light and sconce.", "dcd9cb4775934a4d9572d923a3c8fc2c": "blue and white sphere with floral, cross, and star elements.", 
        "d40f6a7e7dc049a6b9e63c2ac31918f0": "a small village featuring a pond, trees, and a farm in a grassy field.", 
        "8a213b966bb6445e983de414a157aa24": "a rocky island, coral reef, wrecked ship, and snowy landscape with a sled.", 
        "fb531e2a630c45329ccf8b1d4f076996": "a person standing on a green cube.", "578f5a1461a7441aad8a3a92f16ae94e": 
        "White plastic knife", "4bca5e63577c4c4193bfc00a82ce187d": "a black and yellow samurai sword.", 
        "5a0c9e77a109446599b472d0d209fac2": "golden cone-shaped object with a hole in it.", 
        "9991f0431081433497766316a520260c": "a blue coral reef with surrounding geographical features.", 
        "6ed68344c70e41ac86b8d595cb867f9d": "a sea shell, mushrooms, and a wing.", 
        "4edc2f96d8ae4fbeba7f85f8a648adcf": "a torn-apart room with furniture, a wooden table, and a man's head.", 
        "98324481a0554ee1855a2ac1d5d9871d": "a black box and two cubes with a kitchen exhaust hood.", 
        "f13f2141e02b4c34bf889fd0ac0cceb8": "white bust of a man with curly hair.", 
        "1c8f4b91f6fd43bc84c6e3696130035c": "a large ice piece, a flying bird, and various paper-related objects, including shredded paper and a white feather.", 
        "74c05ea2f5d64357a75e4ecafb9570f9": "a blue tank.", 
        "cfd1a14262c9452a98265ff51df738da": "A blue ball with a purple and green crown on it.", 
        "b0e02cd5b642446aadb6517fac83c724": "a small white house.", 
        "64bbe752c13d48dcb699624a64deadae": "a white gun", 
        "f083b065ab434af593a70cfb7b4d37c2": "A blue tray with toothbrushes, toothpaste, and a donut, a blue ring with a pink heart, and a blue bowl filled with toys, alongside a blue ceiling fan with a circular design.", "f154f2372c2542d3915496afac943429": "a small white building resembling a house or office with a ceiling-mounted air conditioner.", 
        "b6550219072d42d2beac49d2b862f50d": "a stack of alternating white and black cubes resembling poker chips or boxes.",
    }
    
    for key, caption in test_data.items():
        print(f"\nCaption: {caption}")
        num_objects = detector.count_objects(caption)
        print(f"Number of objects: {num_objects}")


if __name__ == '__main__':
    # Uncomment the following lines to run the main processing
    input_filename = '../datasets/cap3d_captions.json'
    output_filename = '../filtered/filtered_cap3d_captions.json'
    batch_size = 500
    write_batch_size = 2000

    filtered_data = {}
    total_filtered_count = 0
    first_batch = True
    
    # Count total batches
    total_batches = sum(1 for _ in read_json_in_batches(input_filename, batch_size))
    current_batch = 0

    for batch in read_json_in_batches(input_filename, batch_size):
        current_batch += 1
        filtered_batch = filter_captions(batch)
        filtered_data.update(filtered_batch)
        total_filtered_count += len(filtered_batch)

        if total_filtered_count >= write_batch_size or current_batch == total_batches:
            write_filtered_json(output_filename, filtered_data, first_batch=first_batch, last_batch=(current_batch == total_batches))
            print(f"Wrote batch {current_batch}/{total_batches} with {total_filtered_count} filtered captions")
            filtered_data = {}
            total_filtered_count = 0
            first_batch = False

    print("Filtering and writing completed.")

    # Optionally, you can keep the test function call if you want to run tests
    # test_caption_filtering()