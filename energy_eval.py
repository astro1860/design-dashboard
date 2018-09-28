import json
import requests
import shapely


def energy_gpr_mix(url):
    # energy demand per week Wh/m2/week
    energy_res_u = 1300.655
    energy_off_u = 3232.305
    energy_com_u = 9210.615
    e_res = 0
    e_off = 0
    e_com = 0
    gpr_sum=0
    function_count = []
    data = requests.get(url).text
    b = json.loads(data)
    for i, feature in enumerate(b["geometry"]["features"]):
        p = feature["properties"]
        # Find the feature objects that are not template and camera or other special objects
        if 'special' not in p.keys():
            # Calculate GPR
            gpr_sum += p["height"] * p["SurfaceArea(m2)"]
            function_count.append(p["name"])
            if p["name"] == 'Residential':
                e_res += energy_res_u*p["height"]*p["SurfaceArea(m2)"]
            elif p["name"] == 'Office':
                e_off += energy_off_u*p["height"]*p["SurfaceArea(m2)"]
            elif p["name"] == 'Commercial':
                e_com += energy_com_u*p["height"]*p["SurfaceArea(m2)"]

    energy_demand = e_com + e_res + e_off
    gpr = gpr_sum/200000
    print(energy_demand, gpr)
    occ_res = function_count.count("Residential")
    occ_off = function_count.count('Office')
    occ_com = function_count.count('Commercial')
    occ = [{"name": "Residential", "freq": occ_res},
           {"name": "Office", "freq": occ_off},
           {"name": "Commercial", "freq": occ_com}]
    # occ = {"Residential": occ_res, "Office": occ_off, "Commercial": occ_com}

    # make as the json object/array so that can pass it to .js
    data = [{"f_mixed": occ, "energy": energy_demand, "gpr": gpr}]

    return data