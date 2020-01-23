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
all_recs = ''

def load_model():
    return pd.read_excel("data.xlsx")


def predict(data, X_test):
    return df.to_json(data[data["color"] == X_test["color"]] & (data[data["type"] == X_test["type"]]).sort_values(
        columns="escore", ascending=False)[:3])


def obj_dict(obj):
    return obj.__dict__


@app.route('/', methods=['GET'])
def getResponse():
    global chromeURL, all_recs
    if (chromeURL != ''):
        chromeURL = ''
        return all_recs
    else:
        return json.dumps({'msg': 'No URL'})


@app.route('/url', methods=['GET'])
def getURL():
    global chromeURL
    return chromeURL


@app.route('/data', methods=['GET'])
def get_data():
    global chromeURL
    url = request.args.get('url')
    chromeURL = url
    print(url)
    data = load_model()
    try:
        prod = product.Product(url)
    except Exception:
        if 'Lacoste' in url:
            feat = ['Cotton^Jersey','Imported','Pull On closure','Tumble dry',
                   'Crafted in ultra soft pima cotton, this solid crew neck T shirt offers the perfect combination of casual comfort and classic style',
                   'Fan favorite short sleeve classic crew neck',
                   'Ultra soft pima cotton jersey material',
                   'French born, Lacoste fit is based off of European size conversion, we suggest sizing up for a more relaxed fit',
                   'Signature embroidered green crocodile on left chest','100% Cotton']

            prod = product.Product(url, title='Lacoste Mens Short Sleeve V-Neck Pima Cotton Jersey T-Shirt',
                                   color='white', price=41.70, features=feat,
                                   hierarchy=['', ''], brand='lacoste', composition=['cotton'],
                                   img='https://images-na.ssl-images-amazon.com/images/I/71I4MFqcrSL._AC_UX679_.jpg',
                                   scrape=False)
        elif 'Levi' in url:
            feat = ['100% Cotton','Imported','Pull On closure','Machine Wash','Crew neck']

            prod = product.Product(url, title="Levi's Men's Graphic Logo T-Shirt ",
                                   color='white', price=12.99, features=feat,
                                   hierarchy=['', ''], brand='levis', composition=['cotton'],
                                   img='https://images-na.ssl-images-amazon.com/images/I/714RKFrQwwL._AC_UX679_.jpg',
                                   scrape=False)
        else:
            feat = [
                "SWEAT-WICKING NIKE T-SHIRT STYLE: The Nike Dri-FIT Men's T-Shirt delivers a soft feel, sweat-wicking performance and great range of motion to get you through your workout in total comfort.",
                "NIKE SHIRT: The Nike men's workout shirt has a standard fit for a relaxed, easy feel during physical activity. Small Nike swoosh trademark on left chest.",
                "COMFORTABLE FIT: The Nike Dry fabric material moves with you for optimal range while you play. The Nike shirt for men is crafted with 60% cotton and 40% polyester.",
                "RIBBED CREW NECK: The Nike t-shirt for men has a ribbed crew neck that gives you a comfortable fit when active. The cut is designed to lay smoothly against the skin.",
                "NIKE MEN'S SHIRT: Regular fit, fabric: 60% cotton/40% polyester, imported, machine wash"]

            prod = product.Product(url, title='Nike drift cotton Solid', color='white', price=39.47, features=feat,
                                   hierarchy=['', ''], brand='nike', composition=['cotton', 'polyester'],
                                   img='https://images-na.ssl-images-amazon.com/images/I/610fWFJNkOL._AC_SY450_.jpg',
                                   scrape=False)
    dct = prod.to_dict()

    # return str(lst)
    global all_recs
    all_recs = json.dumps(model.predict(data, dct, prod.scrape))
    return all_recs
    # return json.dumps(RESPONSE, default=obj_dict)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 2700))
    # app.run(host='0.0.0.0', port=port)
    app.run(host='127.0.0.1', port=port, debug=True)
