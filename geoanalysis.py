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
    occ_res = function_count['Residential']
    occ_off = function_count['Office']
    occ_com = function_count['Commercial']

    return energy_demand, gpr


def findname(url):
    data = requests.get(url).text
    b = json.loads(data)
    # b = requests.get(url).json()
    # print(requests.get(url).json())
    name_results = []
    for i, feature in enumerate(b["geometry"]["features"]):
        p = feature["properties"]
        if 'name' in p.keys():
            name_results.append(p["name"])
    print(name_results)

    nhtml = '''<h2>You have used the following elements</h2>'''
    for n in name_results:
        nhtml += '''<h4>''' + str(n)+ '''<br>''' + '''</h4>'''
    return nhtml


def counter(url):
    data = requests.get(url).text
    print(data)
    b = json.loads(data)
    block_list = []
    group = set()

    for i, feature in enumerate(b["geometry"]["features"]):
        p = feature["properties"]
        # we need to merge objects with the same GroupID
        # find distinct groupID
        if 'groupID' in p.keys() and p['groupID'] not in group:
            group.add(p["groupID"])
            p_key = set(p.keys())
            d_set = set(['name','static','visible'])
            dp_set = p_key.intersection(d_set)

            if dp_set == {'name'}:
                # exclude objects: "static": true, "special"(forcedArea, Camera etc.), "visible": false
                block_name = p['name']
                block_list.append(block_name)

    block_set = set(block_list)  # block_set: unique elements
    block_freq = {}  # compute frequency of blocks
    blocks = []
    for name in block_set:
        blocks.append({"name": name, "freq":block_list.count(name)})
    # print(blocks)

    # for name in block_set:
    #     block_freq[name] = block_list.count(name)
    # # sort block name by design frequency
    # blocks = sorted(block_freq.items(), key=lambda d: d[1], reverse=True)
    # blocks = [list(b) for b in blocks]
    #print(blocks)
    #
    # bhtml = '''<h2>You have used the following elements</h2>'''
    # for b in blocks:
    #     bhtml += '''<h4>''' + str(b[0]) + ': ' + str(b[1]) + ' time(s)' + '''<br>''' + '''</h4>'''
    # bhtml += '''<h3>Your have reached the greenery score!</h3>'''
    # bhtml += '''<h3>Your design can't attract enough people</h3>'''
    #return bhtml # for analysis function
    return blocks  # for visualization


# To-do:
# 1. implement the text analyzer
# 2. implement html page for rendering
#
#
# url = 'http://localhost:3000/exercise/4/1/geometry'
# findname(url)
#
# # url='http://localhost:3000/exercise/5/1/geometry'
# # counter(url)