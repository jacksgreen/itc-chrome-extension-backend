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
RESPONSE = ""


def load_model():
    return pd.read_excel("data.xlsx")


def predict(data, X_test):
    return df.to_json(data[data["color"] == X_test["color"]] & (data[data["type"] == X_test["type"]]).sort_values(
        columns="escore", ascending=False)[:3])


def obj_dict(obj):
    return obj.__dict__


@app.route('/', methods=['GET'])
def getResponse():
    global chromeURL
    if (chromeURL != ''):
        url = chromeURL
        chromeURL = ''
        data = model.load_model()
        dct = product.Product(url).to_dict()
        return str(model.predict(data, dct))
    else:
        return json.dumps({'msg': 'No URL'})


@app.route('/url', methods=['GET'])
def getURL():
    global chromeURL
    return chromeURL


@app.route('/icon', methods=['GET'])
def get_icon():
    return json.dumps({"icon": 5})


@app.route('/data', methods=['GET'])
def get_data():
    global chromeURL
    url = request.args.get('url')
    chromeURL = url
    data = load_model()
    try:
        prod = product.Product(url)
    except Exception:
        feat = [
            "SWEAT-WICKING NIKE T-SHIRT STYLE: The Nike Dri-FIT Men's T-Shirt delivers a soft feel, sweat-wicking performance and great range of motion to get you through your workout in total comfort.",
            "NIKE SHIRT: The Nike men's workout shirt has a standard fit for a relaxed, easy feel during physical activity. Small Nike swoosh trademark on left chest.",
            "COMFORTABLE FIT: The Nike Dry fabric material moves with you for optimal range while you play. The Nike shirt for men is crafted with 60% cotton and 40% polyester.",
            "RIBBED CREW NECK: The Nike t-shirt for men has a ribbed crew neck that gives you a comfortable fit when active. The cut is designed to lay smoothly against the skin.",
            "NIKE MEN'S SHIRT: Regular fit, fabric: 60% cotton/40% polyester, imported, machine wash"]

        prod = product.Product(url, title='Nike drift cotton Solid', color='white', price=39.47, features=feat,
                               hierarchy=['', ''], brand='',composition=['cotton','polyester'],
                               img='https://images-na.ssl-images-amazon.com/images/I/610fWFJNkOL._AC_SY450_.jpg',scrape=False)
    dct = prod.to_dict()
    # return str(lst)
    return str(model.predict(data, dct))
    # return json.dumps(RESPONSE, default=obj_dict)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 2700))
    # app.run(host='0.0.0.0', port=port)
    app.run(host='127.0.0.1', port=port, debug=True)
