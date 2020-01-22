from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import json
import os
import requests
import random

app = Flask(__name__)
CORS(app)


RESPONSE = {'msg': 'Success',
            'mainProduct': {'price': '$5', 'titleName': 'White V-neck', 'subTitle': 'Amazon product 1',
                            'ecoScore': '6', 'photoUrl': 'https://shirtsofcotton.com/en/media/catalog/product/cache/10/image/1200x1200/9df78eab33525d08d6e5fb8d27136e95/s/o/soc.02-wit-t-shirt-basic-v-hals.jpg',
                            'details': '100% cotton'},
            'firstSuggestion': {'price': '$7', 'titleName': 'White T-Shirt 1', 'subTitle': 'Amazon product 2',
                                'ecoScore': '3', 'photoUrl': 'data:image/jpeg;base64,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',
                                'details': '90% cotton 10% Plastic'},
            'secondSuggestion': {'price': '$2', 'titleName': 'White T-Shirt 2', 'subTitle': 'Amazon product 3 ',
                                 'ecoScore': '5', 'photoUrl': 'https://5.imimg.com/data5/YB/QU/MY-24671135/blank-t-shirt-500x500.jpg',
                                 'details': '70% cotton'},
            'thirdSuggestion': {'price': '$3', 'titleName': 'White T-Shirt 3', 'subTitle': 'Amazon product 4',
                                'ecoScore': '1', 'photoUrl': 'https://hips.hearstapps.com/vader-prod.s3.amazonaws.com/1553119996-everlane-1553119988.jpg',
                                'details': '10% cotton'},
            }

chromeURL = ''


def obj_dict(obj):
    return obj.__dict__


@app.route('/', methods=['GET'])
def getResponse():
    global RESPONSE, chromeURL
    if(chromeURL != ''):
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
    return json.dumps({"icon": RESPONSE["mainProduct"]["ecoScore"]})


@app.route('/data', methods=['GET'])
def get_data():
    global chromeURL
    url = request.args.get('url')
    chromeURL = url
    return json.dumps(RESPONSE, default=obj_dict)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 2700))
    # app.run(host='0.0.0.0', port=port)
    app.run(host='127.0.0.1', port=port)
