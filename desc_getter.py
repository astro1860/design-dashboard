import json
import requests
import shapely
import math
from operator import itemgetter

def desc_getter(url_desc):
    desc_text = requests.get(url_desc).text
    desc_list = json.loads(desc_text)
    return desc_list