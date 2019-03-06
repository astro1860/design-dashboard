from flask import Flask
from flask import render_template
from flask import request
from energy_eval import energy_gpr_mix
import json
from layoutanalysis import layoutanalysis
from desc_getter import desc_getter
import requests
# Variables
#url = 'https://qua-kit.fcl.sg/exercise/23/443/geometry'


app = Flask(__name__)

# Main Page
@app.route("/")
def index():
    return "Home Page"

# Testing Page: d3.js
# http://localhost:5000/service?url=https://qua-kit.ethz.ch/exercise/33/3485/geometry

@app.route("/test")
def ppprint():
    url = request.args.get('url')
    f_o = json.dumps(layoutanalysis(url))
    url_desc = url.replace('geometry', 'info')
    desc_list = desc_getter(url_desc)['subInfoDescription']
    return render_template("index.html", data=f_o, addr_design=url, desc=desc_list)  # data passed to a web page


#
@app.route("/service_1", methods=['GET','POST'])

def service_1():
    if request.method == "POST":
        #geom = request.value.get('geometry') # get all the parameters
        geom = request.get_json('geometry') # get the geometry in json format (if the previous line doesn't work)
        print("POST DETECTED!")
        geom_list = json.loads(geom)
        f_o = json.dumps(layoutanalysis(geom_list))
        return render_template("index_slim.html", data=f_o)  # data passed to a web page


    elif request.method == "GET":
        url = request.args.get('url')
        file = requests.get(url).text
        b = json.loads(file)  # load: convert json --> python list
        f_o = json.dumps(layoutanalysis(b))
        url_desc = url.replace('geometry', 'info')
        desc_list = desc_getter(url_desc)['subInfoDescription']
        return render_template("index.html", data=f_o, addr_design=url, desc=desc_list)  # data passed to a web page

# def internal():
#     url = request.args.get('url')
#     print(url)
#     f_o = json.dumps(layoutanalysis(url))
#     print(f_o)
#     # data = requests.get(url).text
#     return render_template("index.html", data=f_o, addr_design=url)  # data passed to a web page

if __name__ == "__main__":
    #app.run(host='129.132.32.168', port=5000, debug=True)
    app.run(host='0.0.0.0',port=8000,debug=True)
