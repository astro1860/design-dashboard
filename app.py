from flask import Flask
from flask import render_template
from flask import request
from energy_eval import energy_gpr_mix
import json
from layoutanalysis import layoutanalysis
from layoutservice2 import layoutservice2
from layoutservice3 import layoutservice3
from desc_getter import desc_getter
import requests
import pdb
# Variables
# Variables

app = Flask(__name__)
#app.config.update(MAX_CONTENT_LENGTH=20971520)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024

# Main Page
@app.route("/")
def index():
    return "Home Page"

# Testing Page: d3.js
# http://localhost:8000/service?url=https://qua-kit.ethz.ch/exercise/33/3485/geometry
# http://localhost:8000/test?url=https://qua-kit.ethz.ch/exercise/36/1686/geometry

# http://localhost:8000/test?url=https://qua-kit.ethz.ch/exercise/40/4575/geometry
# url = "https://qua-kit.ethz.ch/exercise/40/4575"
# url = request.args.get('url')
@app.route("/test")
def ppprint():
    url = request.args.get('url')
    print(url)
    file = requests.get(url).text
    #print(file)
    b = json.loads(file)  # load: convert json --> python list
    f_o = json.dumps(layoutservice3(b))
    #print("fo", f_o)
    url_desc = url.replace('geometry', 'info')
    desc_list = desc_getter(url_desc)['subInfoDescription']
    return render_template("index_chi.html", data=f_o, addr_design=url, desc=desc_list)  # data passed to a web page
    #return render_template("index_s1.html", data=f_o)  # data passed to a web page

@app.route("/service_3", methods=['GET','POST'])
def service_3():
    if request.method == "POST":
        print("POST DETECTED!")
        # geom = request.value.get('geometry') # get all the parameters
        #geom = request.get_json('url') # get the geometry in json format (if the previous line doesn't work)
        geom = request.args.get('url')
        print("POST DETECTED and url get!")
        print(geom)
        geom_list = json.loads(geom)
        f_o = json.dumps(layoutservice3(geom_list))
        return render_template("index_chi.html", data=f_o)  # data passed to a web page


    elif request.method == "GET":
        url = request.args.get('url')
        print("GET detected!")
        print(url)
        file = requests.get(url).text
        print(file)
        b = json.loads(file)  # load: convert json --> python list
        f_o = json.dumps(layoutservice3(b))
        url_desc = url.replace('geometry', 'info')
        desc_list = desc_getter(url_desc)['subInfoDescription']
        return render_template("index_chi.html", data=f_o, addr_design=url, desc=desc_list)  # data passed to a web page



@app.route("/service_1")
def service1():
    url = request.args.get('url')
    print(url)
    file = requests.get(url).text
    print(file)
    b = json.loads(file)  # load: convert json --> python list
    f_o = json.dumps(layoutanalysis(b))
    #print("fo", f_o)
    url_desc = url.replace('geometry', 'info')
    desc_list = desc_getter(url_desc)['subInfoDescription']
    return render_template("index.html", data=f_o, addr_design=url, desc=desc_list)  # data passed to a web page
    #return render_template("index_s1.html", data=f_o)  # data passed to a web page


#
@app.route("/service_2", methods=['GET','POST'])
def service_2():
    if request.method == "POST":
        print("POST DETECTED!")
        # geom = request.value.get('geometry') # get all the parameters
        #geom = request.get_json('url') # get the geometry in json format (if the previous line doesn't work)
        geom = request.args.get('url')
        print("POST DETECTED and url get!")
        print(geom)
        geom_list = json.loads(geom)
        f_o = json.dumps(layoutservice2(geom_list))
        return render_template("index_plab_slim.html", data=f_o)  # data passed to a web page


    elif request.method == "GET":
        url = request.args.get('url')
        print("GET detected!")
        print(url)
        file = requests.get(url).text
        print(file)
        b = json.loads(file)  # load: convert json --> python list
        f_o = json.dumps(layoutservice2(b))
        url_desc = url.replace('geometry', 'info')
        desc_list = desc_getter(url_desc)['subInfoDescription']
        return render_template("index_plab.html", data=f_o, addr_design=url, desc=desc_list)  # data passed to a web page

@app.route('/post', methods=('POST',))
def view_post():
    print(request.form["geometry"])
    return request.form["geometry"]

# def internal():
#     url = request.args.get('url')
#     print(url)
#     f_o = json.dumps(layoutanalysis(url))
#     #print(f_o)
#     # data = requests.get(url).text
#     return render_template("index.html", data=f_o, addr_design=url)  # data passed to a web page

if __name__ == "__main__":
    #app.run(host='129.132.32.168', port=5000, debug=True)
    app.run(host='0.0.0.0',port=8000,debug=True)
