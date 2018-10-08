# This is the toy example to compute intersections between ploygons
import json
import requests
import shapely
from shapely.geometry import shape, Polygon,box
from shapely.ops import cascaded_union
import pdb
import math
from operator import itemgetter

# def volume(url):
# Prepare data of area and designdata
#url = "https://qua-kit.ethz.ch/exercise/33/1686/geometry" # This is the geojson data to read as example
file = requests.get(url).text
b = json.loads(file)  # load: convert json --> python list
polys_design = []
site = [] # xmin,xmax,ymin,ymax
for i, f in enumerate(b["geometry"]["features"]):
    p = f["properties"]  # p store all the properties
    geo = f["geometry"]  # geo store {"type": Multipolygon, "coordinate"：[[[],[],[]]]} in 3D

    if 'special' not in p.keys():
        for faces in f["geometry"]["coordinates"]:  # attention two layers
            #pdb.set_trace()
            h_bound = 1000
            #print(faces[0])
            for face in faces[0]:  # one more layer --> face[0]=[ ]
                face_height = face[2]
                if face_height < h_bound:
                    h_bound = face_height
                    # print(h_bound, face)
            if h_bound > 0:
                #print(h_bound)
                #print("this is the ceil surface:", p["name"], faces[0])
                ceil = faces[0]
                #print([(c[0],c[1]) for c in ceil])
                xy_poly = Polygon([(c[0],c[1]) for c in ceil])
                #print ("surface polygon area:", xy_poly.area)
                polys_design.append({"Polygon": xy_poly, "function": p["name"], "height": h_bound})
            # ceilings

    if p["nameID"] == "site":
        #print("site area boundary is:")
        boundx=[]
        boundy=[]
        for faces in f["geometry"]["coordinates"]:
            #print(faces)
            boundx.extend([face[0] for face in faces[0]])
            boundy.extend([face[1] for face in faces[0]])
        # print(boundx)
        xmin=min(boundx)
        xmax=max(boundx)
        ymin=min(boundy)
        ymax=max(boundy)
        site = [xmin, xmax, ymin, ymax]
        #print(site)

#print(polys_design)
site_box = box(xmin,ymin,xmax,ymax)
#print(site_box.area) # wrong surface calcuation in the 3d geometry data

# create grid
gsize = 10
x_num = math.ceil((xmax-xmin) / gsize)
y_num = math.ceil((ymax-ymin) / gsize)
grids = []
#print((xmax-xmin),(ymax-ymin))
for i in range(x_num):
    for j in range(y_num):
        x0 = xmin + i * gsize
        x1 = xmin + (i+1)*gsize
        y0 = ymin + j * gsize
        y1 = ymin + (j+1)*gsize
        grids.append(box(x0, y0, x1, y1))
# print("number of grids on this surface:", len(grids))

# Calculation

volume = 0
gfa = 0
residential = 0
commercial = 0
office = 0

com_res = 0
com_off = 0
off_res = 0
com_off_res = 0
off=0
res=0
com=0
energy_res_u = 67.634
energy_off_u = 168.132
energy_com_u = 478.952
fs = {'Commercial':0 ,'Residential':0, 'Office':0}

for g_pos, grid in enumerate(grids):
    h_max=0.1
    h_min = 10000
    i_area =[]
    functions = []
    f_height = []
    inter = []
    for p_pos, poly in enumerate(polys_design):
        polygon = poly['Polygon']
        # check if there are any polygons inside this grid
        i_id = 0
        h_id = 0
        if grid.intersects(polygon):
            i_area.append(grid.intersection(polygon).area)
            functions.append(poly["function"])
            f_height.append(poly["height"])
            inter.append({'fun':poly["function"],"h":poly["height"]/3}) # should convert it into a good data structure
            #fs = {'commercial':0 ,'residential':0, 'office':0}
            for key, value in fs.items():
                if key == poly["function"]:
                    fs[key] += gsize * gsize * poly["height"] /3

            h = poly["height"]
            if h > h_max:
                h_max = h
                h_id = i_id
                i_id += 1


    if h_max != 0.1:
        h_grid = h_max
        #print(h_grid)
        area = i_area[h_id]
        #area = gsize*gsize
        gfa += area * h_grid/3
        volume += area * h_grid
        #print(volume)

    # 对此grid而言
    # YOU CAN IMPROVE THIS PART OF CODE
    if len(inter) >= 1: # there are more than one polygon intersected with this grid
        # print(inter)
        layer = sorted(inter,key=itemgetter('h'))
        #print("sorted list:",layer)
        low_count=0
        med_count=0
        high_count = 0
        low=[]
        med=[]
        high=[]
        for lay in inter:
            layh = lay['h']
            if layh >= 5.0:
                low_count += 1
                low.append(lay['fun'])
            if layh >=15.0:
                med_count +=1
                med.append(lay['fun'])
            if layh >= 30.0:
                high_count +=1
                high.append(lay['fun'])

        countt = [low_count,med_count,high_count]
        level =[5,15,30]
        #print([low,med,high])
        #print(countt)
        #listt = [low,med,high]
        for ind,val in enumerate([low,med,high]):

            if len(set(val)) == 3:
                com_off_res += 5 * gsize * gsize * countt[ind]

           # elif len(set(val)) == 2:
                #print(val)
            if set(val) == set(['Residential','Commercial']):
                com_res += 5 * gsize * gsize * countt[ind]
            if set(val) == set(['Residential','Office']):
                off_res += 5 * gsize * gsize * countt[ind]
            if set(val) == set(['Commercial','Office']):
                com_off += 5 * gsize * gsize * countt[ind]

            # elif len(set(val)) ==1:

            if set(val) == set(['Commercial']):
                com += 5 * gsize * gsize * countt[ind]
            if set(val) == set(['Residential']):
                res += 5 * gsize * gsize * countt[ind]
            if set(val) == set(['Office']):
                off += 5 * gsize * gsize * countt[ind]
        # seq = [x['h'] for x in inter]
        # h_mix = min(seq)
        #
        # if set(functions) == {"commercial", "residential"}:
        #     com_res += h_mix * gsize * gsize * len(inter)
        # if set(functions) == {"commercial", "office"}:
        #     com_off += h_mix * gsize * gsize * len(inter)
        # if set(functions) == {"office", "residential"}:
        #     off_res += h_mix * gsize * gsize * len(inter)
        #
        # if set(functions) == {"commercial", "residential","office"}:
        #     com_off_res += h_mix * gsize * gsize * len(inter)
        #     if len(set(seq)) == 2:
        #
    # YOU CAN IMPROVE THIS PART OF CODE

    # if h_min != 10000 and len(functions) >1:
    #     if set(functions) == {"residential"}:
    #         residential += 1 / len(functions) * gsize * gsize * h_min / 3 #
    #
    #     if set(function) == {'commercial'}:
    #         commercial += 1 / len(function) * gsize * gsize * h_min / 3
    #     if set(function) == {'residential'}:
    #         residential += 1 / len(function) * gsize * gsize * h_min / 3
    #     if set(function) == {"commercial", "residential"}:
    #     commercial += functions.count("commercial") * gsize*gsize*h_min/3
    #     residential += functions.count("residential") * gsize*gsize*h_min/3
    #     office += functions.count("office") * gsize*gsize*h_min/3
    # # if len(functions) > 1：


    # find 最大高度对应的area
    # 对此grid 完成运算
    # if h_max != 0.1:
    #     h_grid = h_max
    #     area = i_area[h_id]
    #     gfa += area * h_grid/3
    #     volume += area * h_grid
    #     print(volume)

print("Total Volume is:", round(volume))
print("GPR is:", round(volume/site_box.area,2))
print("commercial,residential,office,com_off,off_res,com_res,all")
print(com, res, off,com_off,off_res,com_res, com_off_res)

energy_com = fs['Commercial']*energy_com_u
energy_off = fs['Office']*energy_off_u
energy_res = fs['Residential']*energy_res_u
print("functional mix:",fs)
print("energy demand per type", energy_com, energy_off, energy_res)