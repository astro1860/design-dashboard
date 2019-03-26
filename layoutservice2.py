# This is the toy example to compute intersections between ploygons
import json
import requests
import shapely
from shapely.geometry import shape, Polygon,box, JOIN_STYLE
from shapely.ops import cascaded_union
import pdb
import math
from operator import itemgetter

# this is only for test

# with open('/Users/luha/Projects/payalebar/data/design_data/Untitled.json') as testfile:
# with open('/Users/luha/Projects/payalebar/data/design_data/plab_3types.geojson') as testfile:
#     url_list = json.load(testfile)

#url_list=https://qua-kit.ethz.ch/exercise/36/1686/geometry
# url_list = https://qua-kit.ethz.ch/exercise/36/3353/geometry
#b= url_list

#url is the python list
def layoutservice2(url):
# s = [15,30,45] 5 10 15
# s = [15,30]
    s = [15, 30, 45] # Floor of 5,15,30 levels

    # Prepare data of area and designdata

    b = url

    # url = "https://qua-kit.ethz.ch/exercise/36/3353/geometry" # This is the geojson data to read as example
    # file = requests.get(url).text
    # b = json.loads(file)  # load: convert json --> python list


    polys_design = []
    polys_design_green = []
    polys_design_walkway = []
    polys_design_street = []
    eps = 0.001
    # print(b)
    site = [] # xmin,xmax,ymin,ymax
    for i, f in enumerate(b["geometry"]["features"]):
        p = f["properties"]  # p store all the properties
        geo = f["geometry"]  # geo store {"type": Multipolygon, "coordinate"：[[[],[],[]]]} in 3D
        #pdb.set_trace
        xy_polys = []

        if 'special' not in p.keys() and( p["name"] == "residential" or  p["name"] == "office" or  p["name"] == "commercial"): #only deal with it if it is the building(?)
        # if 'special' not in p.keys():  # only deal with it if it is the building(?)
            #print(p)
            for faces in f["geometry"]["coordinates"]:  # attention two layers
                #h_bound = 1
                face_h = set()

                # find the ceiling surface
                for face in faces[0]:  # one more layer --> face[0]=[ ]
                    face_h.add(face[2]) # add to the set

                if len(face_h) == 1 and list(face_h)[0] > 3: # find the top ceilings
                    #print(h_bound)
                    #print("this is the ceil surface:", p["name"], faces[0])
                    ceil = faces[0]
                    # if list(face_h)[0] > h_bound:
                    #     h_bound = list(face_h)[0]
                    #print([(c[0],c[1]) for c in ceil])
                    small_poly = Polygon([(c[0], c[1]) for c in ceil])
                    if small_poly.is_valid == False:
                        small_poly = small_poly.buffer(0)
                        # small_poly = small_poly.buffer(eps, 1, join_style=JOIN_STYLE.mitre).buffer(-eps, 1, join_style=JOIN_STYLE.mitre)
                    xy_polys.append(small_poly)
                    #print ("surface polygon area:", Polygon([(c[0],c[1])))

            # pdb.set_trace()
            # if len(xy_polys) <= 5:
            xy_poly = cascaded_union(xy_polys)
            # else:
            #     xy_poly = xy_polys[-1]
            #print("polygon area",xy_poly.area)
            polys_design.append({"Polygon": xy_poly, "function": p["name"], "height": int(p["height"])*3,
                                 "footprint": int(p["footprint/m2"]), "length": int(p["length/m"])})



        # Site
        if 'name' in p.keys() and p["name"] == "Site":
            [xmin,ymin,xmax,ymax] = Polygon(f["geometry"]["coordinates"][0][0]).bounds
            # boundx=[]
            # boundy=[]
            # for faces in f["geometry"]["coordinates"]:
            #     #print(faces)
            #     boundx.extend([face[0] for face in faces[0]])
            #     boundy.extend([face[1] for face in faces[0]])
            #print("site area boundary is:")
            # #print(boundx)
            # xmin=min(boundx)
            # xmax=max(boundx)
            # ymin=min(boundy)
            # ymax=max(boundy)
            # site = [xmin, xmax, ymin, ymax]

    #site_box = box(xmin,ymin,xmax,ymax)
    # pdb.set_trace()


        if 'special' not in p.keys() and(p["name"].split()[0] == "green"):
            #print(p)
            polys_design_green.append({"function": p["name"], "footprint": int(p["footprint/m2"]), "length": int(p["length/m"])})

        if 'special' not in p.keys() and(p["name"] == "walkway"):
            #print(p)
            polys_design_walkway.append({"function": p["name"], "footprint": int(p["footprint/m2"]), "length": int(p["length/m"])})

        if 'special' not in p.keys() and(p["name"] == "street"):
            #print(p)
            polys_design_street.append({"function": p["name"], "footprint": int(p["footprint/m2"]), "length": int(p["length/m"])})



    # create grid


    gsize = 10 # change !
    x_num = math.ceil((xmax-xmin) / gsize)
    y_num = math.ceil((ymax-ymin) / gsize)
    grids = []
    for i in range(x_num):
        for j in range(y_num):
            x0 = xmin + i * gsize
            x1 = xmin + (i+1)*gsize
            y0 = ymin + j * gsize
            y1 = ymin + (j+1)*gsize
            grids.append(box(x0, y0, x1, y1))

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
    res_sqm = 0
    com_sqm = 0
    off_sqm = 0
    fs = {'commercial':0 ,'residential':0, 'office':0}

    volume3 = 0
    volume2com_res = 0
    volume2com_off = 0
    volume2res_off = 0
    volume1com = 0
    volume1res = 0
    volume1off = 0
    roof_surface = 0
    for g_pos, grid in enumerate(grids):
        h_max=0.1
        i_area =[]
        functions = []
        f_height = []
        inter = []
        volume4all = {"com":[],"res":[],"off":[]}
        for p_pos, poly in enumerate(polys_design):
            polygon = poly['Polygon']
            # check if there are any polygons inside this grid
            i_id = 0
            h_id = 0
            if grid.intersects(polygon):
                # pdb.set_trace()
                i_area.append(grid.intersection(polygon).area)
                #functions.append(poly["function"])
                #.split()[0]
                functions.append(poly["function"])
                f_height.append(poly["height"])
                # print("intersected")

                # Find which kind of functional polygon it intersected with!
                if poly["function"] == "commercial":
                    volume4all["com"].append(poly["height"])
                    #print(poly["height"])
                    #print("commercial interseced")
                elif poly["function"] == "residential":
                    volume4all["res"].append(poly["height"])
                    #print("res interseced")
                elif poly["function"] == 'office':
                    volume4all["off"].append(poly["height"])
                    #print("off interseced")

                for key, value in fs.items():
                    if key == poly["function"]:
                        fs[key] += gsize * gsize * poly["height"]/3

                h = poly["height"]
                if h > h_max:
                    h_max = h
                    h_id = i_id
                    i_id += 1


        if h_max != 0.1:
            h_grid = h_max
            area = i_area[h_id]
            #print(area)
            #area = gsize*gsize
            gfa += area * h_grid/3
            volume += area * h_grid

        # 对此grid而言
        v_check = {k: v for k, v in volume4all.items() if v != []}
        # add if dictionary is not empty

        if v_check != {}:
            garea = area
            #print("areas:", i_area)
            #print(volume4all)
            for key, all_height in volume4all.items():
                segment =[]
                for val in all_height:
                    if val == 45:
                        segment.extend(["s1"])
                    elif val == 135:
                        segment.extend(["s1", "s2"])
                    elif val == 270:
                        segment.extend(["s1", "s2", "s3"])
                volume4all[key] = segment
            #print("update",volume4all)
            #volume4all = {"com":[s1,s2,s3,s1],"res":[s1,s2],"off":[s1]}

            # 最底层
            s1_com = volume4all["com"].count("s1") # 2
            s1_res = volume4all["res"].count("s1") # 1
            s1_off = volume4all["off"].count("s1") # 1
            s1_count = s1_com+s1_res+s1_off
            # 中间层
            s2_com = volume4all["com"].count("s2")
            s2_res = volume4all["res"].count("s2")
            s2_off = volume4all["off"].count("s2")
            s2_count = s2_com+s2_res+s2_off
            # 最高层
            s3_com = volume4all["com"].count("s3")
            s3_res = volume4all["res"].count("s3")
            s3_off = volume4all["off"].count("s3")
            s3_count = s3_com+s3_res+s3_off

            #BOTOM LAYER
            # 一种相交
            # 第一层
            if (s1_com > 0) & (s1_res == 0) & (s1_off == 0):
                volume1com += (garea * s[0] / 3 * s1_com)/s1_count
                roof_surface += garea
            elif (s1_com == 0) & (s1_res > 0) & (s1_off == 0):
                volume1res += (garea * s[0] / 3 * s1_res)/s1_count
                roof_surface += garea
            elif (s1_com == 0) & (s1_res == 0) & (s1_off > 0):
                volume1off += (garea * s[0] / 3 * s1_off)/s1_count
                roof_surface += garea
            # 两种相交
            # 第一层俩 com res off
            elif (s1_com > 0) & (s1_res > 0) & (s1_off == 0):
                volume2com_res += (garea * s[0] / 3 * (s1_com + s1_res))/s1_count
                res_sqm += volume2com_res * (s1_res/s1_count)
                com_sqm += volume2com_res * (s1_com/s1_count)
                roof_surface += garea
            elif (s1_com > 0) & (s1_res == 0) & (s1_off > 0):
                volume2com_off += (area * s[0] / 3 * (s1_com + s1_off))/s1_count
                com_sqm += volume2com_off * (s1_com / s1_count)
                off_sqm += volume2com_off * (s1_off / s1_count)
                roof_surface += garea
            elif (s1_com == 0) & (s1_res > 0) & (s1_off > 0):
                volume2res_off += (garea * s[0] / 3 * (s1_off + s1_res))/s1_count
                res_sqm += volume2res_off * (s1_res / s1_count)
                com_sqm += volume2res_off * (s1_com / s1_count)
                roof_surface += garea
            # 三种相交
            elif (s1_com > 0) & (s1_res > 0) & (s1_off > 0):
                volume3 += garea * s[0] / 3
                res_sqm += volume3 * s1_res/s1_count
                com_sqm += volume3 * s1_com / s1_count
                off_sqm += volume3 * s1_off / s1_count
                roof_surface += garea

            ## MIDDLE LAYER
            # 一种相交
            if (s2_com > 0) & (s2_res == 0) & (s2_off == 0):
                volume1com += (garea * s[1] / 3 * s2_com)/s2_count
            elif (s2_com == 0) & (s2_res > 0) & (s2_off == 0):
                volume1res += (garea * s[1] / 3 * s2_res)/s2_count
            elif (s2_com == 0) & (s2_res == 0) & (s2_off > 0):
                volume1off += (garea * s[1] / 3 * s2_off)/s2_count
            # 两种相交
            elif (s2_com > 0) & (s2_res > 0) & (s2_off == 0):
                volume2com_res += garea * s[1] / 3
                res_sqm += volume2com_res * (s2_res / s2_count)
                com_sqm += volume2com_res * (s2_com / s2_count)
            elif (s2_com > 0) & (s2_res == 0) & (s2_off > 0):
                volume2com_off += garea * s[1] / 3
                com_sqm += volume2com_off * (s2_com / s2_count)
                off_sqm += volume2com_off * (s2_off / s2_count)
            elif (s2_com == 0) & (s2_res > 0) & (s2_off > 0):
                volume2res_off += (garea * s[1] / 3 * (s2_off + s2_res))/s2_count
                res_sqm += volume2res_off * (s2_res / s2_count)
                com_sqm += volume2res_off * (s2_com / s2_count)
            # 三种相交
            elif (s2_com > 0) & (s2_res > 0) & (s2_off > 0):
                volume3 += garea * s[1] / 3
                res_sqm += volume3 * s2_res / s2_count
                com_sqm += volume3 * s2_com / s2_count
                off_sqm += volume3 * s2_off / s2_count

            ## TOPLAYER
            #一种相交
            if (s3_com > 0) & (s3_res == 0) & (s3_off == 0):
                volume1com += garea * s[2] / 3
            elif (s3_com == 0) & (s3_res > 0) & (s3_off == 0):
                volume1res += garea * s[2] / 3
            elif (s3_com == 0) & (s3_res == 0) & (s3_off > 0):
                volume1off += (garea * s[2] / 3 * s3_off)/s3_count
            # 两种相交
            elif (s3_com > 0) & (s3_res > 0) & (s3_off == 0):
                volume2com_res += garea * s[2] / 3
                res_sqm += volume2com_res * (s3_res / s3_count)
                com_sqm += volume2com_res * (s3_com / s3_count)
            elif (s3_com > 0) & (s3_res == 0) & (s3_off > 0):
                volume2com_off += garea * s[2] / 3
                com_sqm += volume2com_off * (s3_com / s3_count)
                off_sqm += volume2com_off * (s3_off / s3_count)
            elif (s3_com == 0) & (s3_res > 0) & (s3_off > 0):
                volume2res_off += garea * s[2] / 3
                res_sqm += volume2res_off * (s3_res / s3_count)
                com_sqm += volume2res_off * (s3_com / s3_count)
            # 三种相交
            elif (s3_com > 0) & (s3_res > 0) & (s3_off > 0):
                volume3 += garea * s[2] / 3
                res_sqm += volume3 * s3_res / s3_count
                com_sqm += volume3 * s3_com / s3_count
                off_sqm += volume3 * s3_off / s3_count



    #print("volume3",volume3)
    #print("mixed used,(comres,comoff,resoff)",volume2com_res,volume2com_off,volume2res_off)
    #print("single used:(com, off, res)",volume1com,volume1off,volume1res)

    t_volume = (volume3 + volume2com_res+volume2com_off+volume2res_off+volume1com+volume1off+volume1res)*3 # t_volume is the total area surface
    floor_area = t_volume/3
    res_sqm += volume1res
    com_sqm += volume1com
    off_sqm += volume1off
    # weekly
    # unit_res= 0.13 #67.634
    # unit_off = 0.32 # 168.132
    # unit_com = 0.92 # 478.952

    # annual
    unit_res= 67.634
    unit_off = 168.132
    unit_com = 478.952

    res_energy = res_sqm * unit_res
    com_energy = com_sqm * unit_res
    off_energy = off_sqm* unit_off

    res_density = res_sqm*4 /1000 # assume for 1000m2 building, each floor hold max. 4 unit houses

    # print("sqm (res,com,off)is:", res_sqm, com_sqm, off_sqm)
    # print("energy (res,com,off) is:", res_energy,com_energy,off_energy)
    # print("resident population is", res_density)
    #
    # print("***********")
    # print("method1 added volume:",(volume3 + volume2com_res+volume2com_off+volume2res_off+volume1com+volume1off+volume1res)*3)
    #
    # print("Total Volume is:", volume)
    # print("GPR is:", round(volume/site_box.area,2))
    # print("commercial,residential,office,com_off,off_res,com_res,all")
    ccode = ["#b24343","#f9bb52","#89a3c2","#6c4c87","#3d8677","#e499bd","#bfbfbf"]

    occ = [{"name": "Residential", "freq": volume1res, "color":ccode[0]},
           {"name": "Office", "freq": volume1off,"color":ccode[1]},
           {"name": "Commercial", "freq": volume1com,"color":ccode[2]},
           {"name": "Mixed: Commercial&Residential","freq":volume2com_res,"color":ccode[3]},
           {"name": "Mixed: Commercial&Office","freq":volume2com_off,"color":ccode[4]},
           {"name": "Mixed: Residential&Office","freq":volume2res_off,"color":ccode[5]},
           {"name": "Mixed: Commercial&Residential&Office", "freq": volume3,"color":ccode[6]}
           ]

    # Single Use:
    occ_single = [{"name": "Residential", "freq": volume1res, "color":ccode[0]},
           {"name": "Office", "freq": volume1off,"color":ccode[1]},
           {"name": "Commercial", "freq": volume1com,"color":ccode[2]}]

    func_single = [occ_item for occ_item in occ_single if occ_item["freq"]!=0]

    # Mixed Use:
    occ_mixed = [{"name": "Mixed: Commercial&Residential","freq":volume2com_res,"color":ccode[3]},
           {"name": "Mixed: Commercial&Office","freq":volume2com_off,"color":ccode[4]},
           {"name": "Mixed: Residential&Office","freq":volume2res_off,"color":ccode[5]},
           {"name": "Mixed: Commercial&Residential&Office", "freq": volume3,"color":ccode[6]}]

    func_mix_only = [occ_item for occ_item in occ_mixed if occ_item["freq"]!=0]

    # All together"
    func_mix = [occ_item for occ_item in occ if occ_item["freq"]!=0]

    energy_demand= res_energy+com_energy+off_energy
    gpr = floor_area/1000000

    construction = len(polys_design)

    # pdb.set_trace()
    def dic_key(dic):
        return dic['freq']
    max_name = max(func_mix,key=dic_key)["name"]
    #print("largest1:",max_name)


    energy_data = [{"name":"Residential","value":res_energy,"color":ccode[0]},
                   {"name":"Office","value": off_energy,"color":ccode[1]},
                   {"name":"Commercial","value": com_energy,"color":ccode[2]}]

    area_data = [{"name":"Residential","value":res_sqm,"color":ccode[0]},
                 {"name":"Office","value": off_sqm,"color":ccode[1]},
                 {"name":"Commercial","value": com_sqm,"color":ccode[2]}]


    f_percent = ["{:.2%}".format(x["freq"]/floor_area) for x in func_mix]
    f_percent_single = ["{:.2%}".format(x["freq"]/(volume1res+volume1off+volume1com)) for x in func_single]
    f_percent_mix = ["{:.2%}".format(x["freq"]/(volume2com_res+volume2com_off+volume2res_off+volume3)) for x in func_mix_only]

    # Calculate of GreenSpaces
    # Calculate of Lanes
    # print(polys_design)
    lanes = 0
    green = 0
    network_area = 0

    for pid, poly in enumerate(polys_design_green):
        green += int(poly["footprint"])

    for pid, poly in enumerate(polys_design_walkway):
        network_area += int(poly["footprint"])
        lanes += int(poly["length"])

    for pid, poly in enumerate(polys_design_street):
        network_area += int(poly["footprint"])
        lanes += int(poly["length"])

        # if there is any overlaps of green areas
        # To-do
    # print("Total green area is", green)
    # print("Total road length is", lanes)
    # print("Total road area is", network_area)
    # print("total roof area is (m2)", roof_surface)
    green_rate = green /1000000 *100
    road_rate = network_area/1000000 *100

    #pdb.set_trace()
    # PV energy production in kWh
    energy_pv = roof_surface * 0.75 * 0.15 * 800 * 0.75
    #print("Active annual energy production (in kWh)by PV installation is:",energy_pv)
    #print("Annual Energy consumption (in KWh)of the total area is:", energy_demand)
    # data = [{"f_mixed": func_mix,"max_name":max_name,"f_percent": f_percent, "energy_data":energy_data,"area_data":area_data,
    #          "energy_demand":energy_demand,"gpr": gpr,"construction":construction,"floor_area":floor_area,"res_population":res_density,
    #           "total_volume":t_volume, "green_rate": green_rate, "road_rate": road_rate,"road_len": lanes, "energy_pv": energy_pv}]

    data = [{"f_mixed": func_mix,"f_single":func_single,"f_mixed_only":func_mix_only, "max_name":max_name,"f_percent": f_percent, "f_percent_single":f_percent_single, "f_percent_mix":f_percent_mix,"energy_data":energy_data,"area_data":area_data,
             "energy_demand":energy_demand,"gpr": gpr,"construction":construction,"floor_area":floor_area,"res_population":res_density,
              "total_volume":t_volume, "green_rate": green_rate, "road_rate": road_rate,"road_len": lanes, "energy_pv": energy_pv}]

    print(data)
    return data

#layoutservice2(url_list)
#pdb.set_trace()
## SO DAMMED MANY TO DO THINGS WHY I DO I T ALONE MALEGEBI!
# - GREEN SPACES?? RATIO
# - ROAD: HOW LONG AND HOW MANY ROAD DID YOU BUILD??
# - ACTIVE ENERGY PV |  HOW MUCH IT WOULD COST?
# - ENERGY CONSUMPTION
# - HOW MANY WORKPLACE + RESIDENTS REQUIREMENT(!)
