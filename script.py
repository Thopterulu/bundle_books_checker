import requests
import json
import os

OUTPUT_DIR = "output"
RES_FILE_PATH = os.path.join(OUTPUT_DIR, "res.json")


if os.path.exists(OUTPUT_DIR) is False:
    os.mkdir(OUTPUT_DIR)


# we start with humble bundle #

###### vars ########### TODO => vars inside a json conf file
START_OF_HUMBLE_JSON = "<script id=\"landingPage-json-data\" type=\"application/json\">"
END_OF_HUMBLE_PAGE = """</script>


<script src="https://cdn.humblebundle.com/static/hashed/69063536ca3b4f593914fc7bc74a4d625bc69de8.js"></script>
<script src="https://cdn.humblebundle.com/static/hashed/43a729e972775787e82d18d953c70defb3551215.js"></script>

<div id="site-modal"></div>
  </body>
</html>"""
HUMBLE_POPPING_KEYS_LIST = [
    "disable_hero_tile",
    'highlights',
    'bundles_sold|decimal',
    'tile_image_information',
    "hover_title",
    "tile_logo_information",
    "high_res_tile_image",
    "high_res_tile_image_information",
    "fallback_store_sale_logo",
    "supports_partners",
    "machine_name",
    "type"
    ]

###############################

r = requests.get('https://www.humblebundle.com/books')
text = r.text



text = text[r.text.find(START_OF_HUMBLE_JSON) + len(START_OF_HUMBLE_JSON) + 1:]
text = text[:text.find(END_OF_HUMBLE_PAGE)- 1]


def load_json():
    if os.path.exists(RES_FILE_PATH):
        with open(RES_FILE_PATH, "r", encoding="utf-8") as open_file:
            if os.path.getsize(RES_FILE_PATH) == 0:
                print("file is empty")
                return {}
            return json.load(open_file)

def write_json(RES_FILE, file_name):
    with open(os.path.join(OUTPUT_DIR, f"{file_name}.json"), "w+", encoding="utf-8") as open_file:
        json.dump(RES_FILE, open_file, indent=4, sort_keys=True)

if __name__ == "__main__":
    RES_FILE = {}
    if load_json() != {}:
        RES_FILE = load_json()

    HUMBLE_BOOKS = json.loads(text)["data"]["books"]["mosaic"][0]["products"]
    for a_key, a_value in enumerate(HUMBLE_BOOKS):
        for key in HUMBLE_POPPING_KEYS_LIST:
            HUMBLE_BOOKS[a_key].pop(key)
    #print(RES_FILE)
    write_json(HUMBLE_BOOKS, "humble")


