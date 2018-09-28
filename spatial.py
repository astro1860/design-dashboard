import json
import requests
import shapely

def area(url):
    data = requests.get(url).text
    print(data)
    b = json.loads(data)
    block_list = []
    group = set()

    for i, feature in enumerate(b["geometry"]["features"]):
        p = feature["properties"]