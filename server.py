from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import json
import os
import requests
import random
import model
import product
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)


chromeURL = ''

def obj_dict(obj):
    return obj.__dict__


@app.route('/', methods=['GET'])
def getResponse():
    global RESPONSE, chromeURL
    if (chromeURL != ''):
        chromeURL = ''
        return json.dumps(RESPONSE, default=obj_dict)
    else:
        return json.dumps({'msg': 'No URL'})


@app.route('/url', methods=['GET'])
def getURL():
    global chromeURL
    return chromeURL


@app.route('/icon', methods=['GET'])
def get_icon():
    global RESPONSE
    return json.dumps({"icon": RESPONSE["mainProduct"]["ecoscore"]})


@app.route('/data', methods=['GET'])
def get_data():
    global chromeURL
    url = request.args.get('url')
    chromeURL = url
    data = model.load_model()
    dct = product.Product(url).to_dict()
    #return str(lst)
    return str(model.predict(data, dct))
    # return json.dumps(RESPONSE, default=obj_dict)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 2700))
    # app.run(host='0.0.0.0', port=port)
    app.run(host='127.0.0.1', port=port, debug=True)
