import json
import requests
import shapely
from shapely.geometry import shape, Polygon,box, JOIN_STYLE
from shapely.ops import cascaded_union
import pdb
import math
from operator import itemgetter

def layoutservice_cube(url):
    # url = "https://qua-kit.ethz.ch/exercise/41/4733/geometry" # This is the geojson data to read as example
    # file = requests.get(url).text
    # b = json.loads(file)  # load: convert json --> python list

    b = url

    res = 0
    mixed = 0
    civic = 0
    sport = 0
    green = 0 

    polys_design = []

    for i, f in enumerate(b["geometry"]["features"]):
        p = f["properties"]  # p store all the properties
        geo = f["geometry"]  # geo store {"type": Multipolygon, "coordinate"：[[[],[],[]]]} in 3D
        xy_polys = []
        
        # Site
        # if 'name' in p.keys() and p["name"] == "Site":
        #     [xmin,ymin,xmax,ymax] = Polygon(f["geometry"]["coordinates"][0]).bounds
        
        #1.residential
        if 'special' not in p.keys() and(p["nameID"].split('_')[0] == "res"):
            res += int(p["footprint/m2"]) * 8
        
        #2.mixed
        if 'special' not in p.keys() and(p["nameID"].split('_')[0] == "mixed"):
            mixed += int(p["footprint/m2"]) * 6
        
        #3.civic
        if 'special' not in p.keys() and(p["nameID"].split('_')[0] == "civic"):
            civic += int(p["footprint/m2"]) * 6 
    
        #4.sport
        if 'special' not in p.keys() and(p["nameID"].split('_')[0] == "sport"):
            sport += int(p["footprint/m2"]) * 6 
        
        #5.greenery 
        if 'special' not in p.keys() and(p["nameID"].split('_')[0] == "buildgreen"):
            green += int(p["footprint/m2"])
        if 'special' not in p.keys() and(p["name"].split()[0] == "green"):
            green += int(p["footprint/m2"]) 
        
        
    data = [{"res":res, "mixed":mixed, "civic":civic, "sport":sport, "green":green}]

    print(data)
    return(data)