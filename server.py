from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import json
import os
import requests
import random

app = Flask(__name__)
CORS(app)


RESPONSE = {
    'mainProduct': {'price': '$5', 'titleName': 'White V-neck', 'subTitle': 'Amazon product 1',
                    'ecoScore': '6', 'photoUrl': 'https://shirtsofcotton.com/en/media/catalog/product/cache/10/image/1200x1200/9df78eab33525d08d6e5fb8d27136e95/s/o/soc.02-wit-t-shirt-basic-v-hals.jpg',
                    'details': '100% cotton'},
    'firstSuggestion': {'price': '$7', 'titleName': 'White T-Shirt 1', 'subTitle': 'Amazon product 2',
                        'ecoScore': '3', 'photoUrl': 'https://cowesclothing.com/uploaded/thumbnails/16823185/rna1-white-(A)_16823185_1080xauto.png',
                        'details': '90% cotton 10% Plastic'},
    'secondSuggestion': {'price': '$2', 'titleName': 'White T-Shirt 2', 'subTitle': 'Amazon product 3 ',
                         'ecoScore': '5', 'photoUrl': 'https://5.imimg.com/data5/YB/QU/MY-24671135/blank-t-shirt-500x500.jpg',
                         'details': '70% cotton'},
    'thirdSuggestion': {'price': '$3', 'titleName': 'White T-Shirt 3', 'subTitle': 'Amazon product 4',
                        'ecoScore': '1', 'photoUrl': 'https://hips.hearstapps.com/vader-prod.s3.amazonaws.com/1553119996-everlane-1553119988.jpg',
                        'details': '10% cotton'},
}

chromeURL =''

def obj_dict(obj):
    return obj.__dict__

@app.route('/', methods=['GET'])
def getResponse():
    global RESPONSE
    return json.dumps(RESPONSE, default=obj_dict)


@app.route('/url', methods=['GET'])
def getURL():
    global chromeURL
    return chromeURL


@app.route('/icon', methods=['GET'])
def get_icon():
    global RESPONSE
    return json.dumps({"icon": RESPONSE["mainProduct"]["ecoScore"]})


@app.route('/data', methods=['GET'])
def get_data():
    global chromeURL
    url = request.args.get('url')
    chromeURL = url
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    img = soup.find("img")
    src = img["src"]
    return json.dumps({"src": src})


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 2700))
    app.run(host='0.0.0.0', port=port)
    # app.run(host='127.0.0.1', port=port)
