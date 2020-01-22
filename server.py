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
            'mainProduct': {'brand': '2UNDR', 'title': "2UNDR Men's Luxury V-Neck Tees", 'composition': ['modal', 'polyester'], 'type': 'T-Shirts', 'parent_type': 'Shirts', 'price': 39.98, 'features': ['No Closure closure', 'Classic V-neck', 'Modal/Poly blend', 'Ordr resistant material'], 'ecoscore': 1, 'photoUrl': 'https://images-na.ssl-images-amazon.com/images/I/71h1rgjhwvL._AC_UX679_.jpg', 'url': 'https://www.amazon.com/2UNDR-Mens-Luxury-V-Neck-X-Large/dp/B07JPB1BP1?pf_rd_p=700385e0-19d0-4b4c-89bf-06e23d6f1594&pd_rd_wg=eSwIV&pf_rd_r=VFZ0Z500YC2MQNGBJPD2&ref_=pd_gw_cr_simh&pd_rd_w=qoyy2&pd_rd_r=01e7c99b-25a4-4083-a5af-7ad97e1cf51b'},
            'firstSuggestion': {'brand': '2UNDR', 'title': "2UNDR Men's Luxury V-Neck Tees", 'composition': ['modal', 'polyester'], 'type': 'T-Shirts', 'parent_type': 'Shirts', 'price': 39.98, 'features': ['No Closure closure', 'Classic V-neck', 'Modal/Poly blend', 'Ordr resistant material'], 'ecoscore': 1, 'photoUrl': 'https://images-na.ssl-images-amazon.com/images/I/71h1rgjhwvL._AC_UX679_.jpg', 'url': 'https://www.amazon.com/2UNDR-Mens-Luxury-V-Neck-X-Large/dp/B07JPB1BP1?pf_rd_p=700385e0-19d0-4b4c-89bf-06e23d6f1594&pd_rd_wg=eSwIV&pf_rd_r=VFZ0Z500YC2MQNGBJPD2&ref_=pd_gw_cr_simh&pd_rd_w=qoyy2&pd_rd_r=01e7c99b-25a4-4083-a5af-7ad97e1cf51b'},
            'secondSuggestion': {'brand': '2UNDR', 'title': "2UNDR Men's Luxury V-Neck Tees", 'composition': ['modal', 'polyester'], 'type': 'T-Shirts', 'parent_type': 'Shirts', 'price': 39.98, 'features': ['No Closure closure', 'Classic V-neck', 'Modal/Poly blend', 'Ordr resistant material'], 'ecoscore': 1, 'photoUrl': 'https://images-na.ssl-images-amazon.com/images/I/71h1rgjhwvL._AC_UX679_.jpg', 'url': 'https://www.amazon.com/2UNDR-Mens-Luxury-V-Neck-X-Large/dp/B07JPB1BP1?pf_rd_p=700385e0-19d0-4b4c-89bf-06e23d6f1594&pd_rd_wg=eSwIV&pf_rd_r=VFZ0Z500YC2MQNGBJPD2&ref_=pd_gw_cr_simh&pd_rd_w=qoyy2&pd_rd_r=01e7c99b-25a4-4083-a5af-7ad97e1cf51b'},
            'thirdSuggestion': {'brand': '2UNDR', 'title': "2UNDR Men's Luxury V-Neck Tees", 'composition': ['modal', 'polyester'], 'type': 'T-Shirts', 'parent_type': 'Shirts', 'price': 39.98, 'features': ['No Closure closure', 'Classic V-neck', 'Modal/Poly blend', 'Ordr resistant material'], 'ecoscore': 1, 'photoUrl': 'https://images-na.ssl-images-amazon.com/images/I/71h1rgjhwvL._AC_UX679_.jpg', 'url': 'https://www.amazon.com/2UNDR-Mens-Luxury-V-Neck-X-Large/dp/B07JPB1BP1?pf_rd_p=700385e0-19d0-4b4c-89bf-06e23d6f1594&pd_rd_wg=eSwIV&pf_rd_r=VFZ0Z500YC2MQNGBJPD2&ref_=pd_gw_cr_simh&pd_rd_w=qoyy2&pd_rd_r=01e7c99b-25a4-4083-a5af-7ad97e1cf51b'},
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
