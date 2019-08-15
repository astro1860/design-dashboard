import shapely
from shapely.geometry import shape, Polygon,box, JOIN_STYLE
from shapely.ops import cascaded_union
import pdb
import math
from operator import itemgetter

def polycal(b):
    polys_design = []
    polys_design_green = []
    polys_design_walkway = []
    polys_design_street = []
    polys_design_shade =[] 
    polys_design_park=[] 
    polys_design_play=[] 
    polys_design_rooftree =[] 
    for i, f in enumerate(b["geometry"]["features"]):
        p = f["properties"]  # p store all the properties
        geo = f["geometry"]  # geo store {"type": Multipolygon, "coordinate"：[[[],[],[]]]} in 3D
        xy_polys = []
        
        # eliminate the static ones # and 'static' not in p.keys()
        if 'special' not in p.keys() and(p["name"] == "residential" or  p["name"] == "office" or  p["name"] == "commercial"): 
            for faces in f["geometry"]["coordinates"]:  # attention two layers
                face_h = set()
                # find the ceiling surface
                for face in faces[0]:  # one more layer --> face[0]=[ ]
                    face_h.add(face[2]) # add to the set

                if len(face_h) == 1 and list(face_h)[0] > 3: # find the top ceilings
                    ceil = faces[0]
                    small_poly = Polygon([(c[0], c[1]) for c in ceil])
                    if small_poly.is_valid == False:
                        small_poly = small_poly.buffer(0)
                    xy_polys.append(small_poly)
            xy_poly = cascaded_union(xy_polys)
            polys_design.append({"Polygon": xy_poly, "function": p["name"], "height": int(p["height"]),
                                 "footprint": int(p["footprint/m2"]), "length": int(p["length/m"])})
        # Site
        if 'name' in p.keys() and p["name"] == "Site":
            [xmin,ymin,xmax,ymax] = Polygon(f["geometry"]["coordinates"][0]).bounds
        #green
        if 'special' not in p.keys() and(p["name"].split()[0] == "green"):
            polys_design_green.append({"function": p["name"], "footprint": int(p["footprint/m2"]), "length": int(p["length/m"])})
        #walkway
        if 'special' not in p.keys() and(p["name"].split()[0] == "walkway"):
            polys_design_walkway.append({"function": p["name"], "footprint": int(p["footprint/m2"]), "length": int(p["length/m"])})
        #street
        if 'special' not in p.keys() and(p["name"].split()[0] == "street"):
            polys_design_street.append({"function": p["name"], "footprint": int(p["footprint/m2"]), "length": int(p["length/m"])})
        #shading
        if 'special' not in p.keys() and(p["name"] == "Shading Single Unit" and p["function"]=="platform"):
            polys_design_shade.append({"function": p["name"], "footprint": 1})
        if 'special' not in p.keys() and(p["name"] == "Shading Multiple units" and p["function"]=="platform"):
            polys_design_shade.append({"function": p["name"], "footprint": 1})
        #rooftree        
        if 'special' not in p.keys() and (p["name"].split()[0] == "roof_trees" and p["function"]=="platform"):
            polys_design_rooftree.append({"function": p["name"], "footprint": 1})
        #playground
        if 'special' not in p.keys() and(p["name"] == "Playground" and p["function"]=="platform"):
            polys_design_play.append({"function": p["name"], "footprint": 1})
        #park
        if 'special' not in p.keys() and(p["name"] == "Park" and p["function"]=="platform"):
            polys_design_park.append({"function": p["name"], "footprint": 1})
    return xmin,ymin,xmax,ymax,polys_design, polys_design_green, polys_design_walkway, polys_design_street, polys_design_shade, polys_design_park, polys_design_play, polys_design_rooftree