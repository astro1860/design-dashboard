from flask import Flask
from flask import render_template
from flask import request
from energy_eval import energy_gpr_mix
import json
from layoutanalysis import layoutanalysis
from desc_getter import desc_getter

# Variables
#url = 'https://qua-kit.fcl.sg/exercise/23/443/geometry'

app = Flask(__name__)

# Main Page
@app.route("/")
def index():
    return "test home page"

# Testing Page: d3.js
# http://localhost:5000/print?url=https://qua-kit.fcl.sg/exercise/23/443/geometry


@app.route("/service")

def ppprint():
    url = request.args.get('url')
    f_o = json.dumps(layoutanalysis(url))
    url_desc = url.replace('geometry', 'info')
    desc_list = desc_getter(url_desc)['subInfoDescription']
    return render_template("index.html", data=f_o, addr_design=url, desc=desc_list)  # data passed to a web page



@app.route("/internal")

def internal():
    url = request.args.get('url')
    print(url)
    f_o = json.dumps(layoutanalysis(url))
    print(f_o)
    # data = requests.get(url).text
    return render_template("index.html", data=f_o, addr_design=url)  # data passed to a web page

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
