# This is the toy example to compute intersections between ploygons
import json
import requests
import shapely
from shapely.geometry import shape, Polygon,box, JOIN_STYLE
from shapely.ops import cascaded_union
import pdb
import math
from operator import itemgetter
from building import building
from polycal import polycal
# this is only for test

with open('/Users/luha/Projects/payalebar/data/chi_design/testfiles/chi_static_add_1.json') as testfile:    
    url = json.load(testfile)


def layoutservice3_file(url):
    # url = "https://qua-kit.ethz.ch/exercise/36/3353/geometry" # This is the geojson data to read as example
    # file = requests.get(url).text
    # b = json.loads(file)  # load: convert json --> python list

    b = url
    xmin,ymin,xmax,ymax, polys_design, polys_design_green, polys_design_walkway, polys_design_street, polys_design_shade, polys_design_park, polys_design_play, polys_design_rooftree = polycal(b)  
    volume3,volume2com_res,volume2com_off,volume2res_off,volume1com,volume1off,volume1res,roof_surface,res_deck = building(xmin,ymin,xmax,ymax,polys_design)
    
    # functions volumn density calculation 
    res_sqm = 0
    com_sqm = 0
    off_sqm = 0
    t_volume = (volume3 + volume2com_res+volume2com_off+volume2res_off+volume1com+volume1off+volume1res)*3 # t_volume is the total area surface
    floor_area = t_volume/3
    res_sqm += volume1res
    com_sqm += volume1com
    off_sqm += volume1off
    res_density = res_sqm*4 /1000 # assume for 1000m2 building, each floor hold max. 4 unit houses
    gpr = floor_area/660000
    construction = len(polys_design)
   
    # annual energy consumption 
    unit_res= 67.634
    unit_off = 168.132
    unit_com = 478.952
    res_energy = res_sqm * unit_res
    com_energy = com_sqm * unit_res
    off_energy = off_sqm* unit_off
    energy_demand= res_energy+com_energy+off_energy
    energy_pv = roof_surface * 0.75 * 0.15 * 800 * 0.75     # PV energy production in kWh

    # Color coding 
    ccode = ["#b24343","#f9bb52","#89a3c2","#6c4c87","#3d8677","#e499bd","#bfbfbf"]
    occ = [{"name": "Residential", "freq": volume1res, "color":ccode[0]},
           {"name": "Office", "freq": volume1off,"color":ccode[1]},
           {"name": "Commercial", "freq": volume1com,"color":ccode[2]},
           {"name": "Mixed: Commercial&Residential","freq":volume2com_res,"color":ccode[3]},
           {"name": "Mixed: Commercial&Office","freq":volume2com_off,"color":ccode[4]},
           {"name": "Mixed: Residential&Office","freq":volume2res_off,"color":ccode[5]},
           {"name": "Mixed: Commercial&Residential&Office", "freq": volume3,"color":ccode[6]}
           ]
    func_mix = [occ_item for occ_item in occ if occ_item["freq"]!=0]
    def dic_key(dic):
        return dic['freq']
    max_name = max(func_mix,key=dic_key)["name"]
    energy_data = [{"name":"Residential","value":res_energy,"color":ccode[0]},
                   {"name":"Office","value": off_energy,"color":ccode[1]},
                   {"name":"Commercial","value": com_energy,"color":ccode[2]}]

    area_data = [{"name":"Residential","value":res_sqm,"color":ccode[0]},
                 {"name":"Office","value": off_sqm,"color":ccode[1]},
                 {"name":"Commercial","value": com_sqm,"color":ccode[2]}]
    f_percent = ["{:.2%}".format(x["freq"]/floor_area) for x in func_mix]

    # Calculate of GreenSpaces, road, shading, parks etc. 
    lanes = 0
    green = 0
    network_area = 0
    shade = 0
    park = 0
    rooftree=0
    play=0
    for pid, poly in enumerate(polys_design_green):
        green += int(poly["footprint"])

    for pid, poly in enumerate(polys_design_walkway):
        network_area += int(poly["footprint"])
        lanes += int(poly["length"])

    for pid, poly in enumerate(polys_design_street):
        network_area += int(poly["footprint"])
        lanes += int(poly["length"])

    for pid, poly in enumerate(polys_design_shade):
        shade += int(poly["footprint"])

    for pid, poly in enumerate(polys_design_rooftree):
        rooftree += int(poly["footprint"])        

    for pid, poly in enumerate(polys_design_park):
        park += int(poly["footprint"])
        

    for pid, poly in enumerate(polys_design_play):
        play += int(poly["footprint"])
    green_rate = green /660000 *100
    road_rate = network_area/660000 *100

    # Mitgation stragtgie Calcuation (Annd cost)
    # 01.GreenFacade:
    greenroof_unit = 1125
    greenfacade = rooftree * greenroof_unit # in square meters
    # 02.Green streetscape
    greenstreet = green+ 1250* park # didnt consider overlap
    # 03. Shading
    shadearea = shade * 625
    # 04. Building Voids(Assuming each floor of residential building contains a void deck)
    void = res_deck * 0.8 
    # 05. solar panels
    roof_left = roof_surface - greenfacade

    st_all = greenfacade + greenstreet + shadearea + void + roof_left
    print("Mitigation Stratgy Intensity:")
    print("green facade:{:.2%}".format(greenfacade/st_all))
    print("green streetscape:{:.2%}".format(greenstreet/st_all))
    print("shading:{:.2%}".format(shadearea/st_all))
    print("void deck:{:.2%}".format(void/st_all))
    print("max solar panels:{:.2%}".format(roof_left/st_all))

    #final data 
    data = [{"f_mixed": func_mix,"max_name":max_name,"f_percent": f_percent, "energy_data":energy_data,"area_data":area_data,
             "energy_demand":energy_demand,"gpr": gpr,"construction":construction,"floor_area":floor_area,"res_population":res_density,
              "total_volume":t_volume, "green_rate": green_rate, "road_rate": road_rate,"road_len": lanes, "energy_pv": energy_pv,
              "rooftree":rooftree,"shade":shade,"playground":play,"park":park}]
    
    
    print(data)    
    
    return data


layoutservice3_file(url)
pdb.set_trace()
'''
# TO-DO
1. Calculate mitigation stratgies intensity 
- solar panel areas (how many areas are covered by roof trees?)
- building voids 
- esitmate the cost

2. Web-UI layout ！

3. Fairness Measurement! 
'''