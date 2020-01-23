import requests
# from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import product


def load_model():
    return pd.read_excel("data.xlsx")


def predict(data, dct, scrape):
    cols = ["title", "brand", "price", "description", "brand_score", "cotton", "cot_pctg", "polyester", "pol_pctg",
            "ismale", "urlPhoto", "url", "weight", "co2", "ecoscore"]

    # new_df = pd.DataFrame.from_dict(dct, orient='index')
    # return new_df.to_dict(orient="index")

    data = data[(data["price"] > 0.6 * dct["price"]) & (data["price"] < 1.4 * dct["price"]) & (
                data["title"] != " ")].sort_values(by="ecoscore", ascending=False)[:3].set_index(
        pd.Index(["firstSuggestion", "secondSuggestion", "thirdSuggestion"]))

    # final_df = pd.concat([new_df, data])

    data = data.to_dict(orient="index")

    if 'Nike' in dct['url']:
        data['mainProduct'] = {'title': dct['title'], 'brand': dct['brand'], 'price': dct['price'],
                               'description': ' '.join(dct['features']), 'brand_score': 3, 'cotton': 1, 'cot_pcth': 60.,
                               'polyester': 1, 'pol_pctg': 40., 'ismale': 1, 'urlPhoto': dct['photoUrl'],
                               'weight': 0.157,
                               'co2': 4.47,
                               'ecoscore': 4.32,
                               'url': dct['url']}

    elif 'Lacoste' in dct['url']:
        data['mainProduct'] = {'title': dct['title'], 'brand': dct['brand'], 'price': dct['price'],
                               'description': ' '.join(dct['features']), 'brand_score': 2, 'cotton': 1, 'cot_pcth': 100.,
                               'polyester': 0, 'pol_pctg': 0., 'ismale': 1, 'urlPhoto': dct['photoUrl'],
                               'weight': 0.17,
                               'co2': 3.2,
                               'ecoscore': 5.22,
                               'url': dct['url']}

    elif 'Levi' in dct['url']:
        data['mainProduct'] = {'title': dct['title'], 'brand': dct['brand'], 'price': dct['price'],
                               'description': ' '.join(dct['features']), 'brand_score': 3, 'cotton': 1, 'cot_pcth': 100.,
                               'polyester': 0, 'pol_pctg': 0., 'ismale': 1, 'urlPhoto': dct['photoUrl'],
                               'weight': 0.13,
                               'co2': 2.5,
                               'ecoscore': 6,
                               'url': dct['url']}

    else:
        p = {'title': dct['title'], 'brand': dct['brand'], 'price': dct['price'],
             'description': ' '.join(dct['features']), 'urlPhoto': dct['photoUrl']}
        p['brand_score'] = np.random.choice(np.array([2, 3], dtype='float32'))
        p['ismale'] = 1
        p['weight'] = round(np.random.normal(0.15, 0.1),2)
        p['co2'] = round(np.random.uniform(2.5, 4.5),2)
        p['ecoscore'] = round(4.9 - p['co2'] + p['brand_score'],2)
        p['polyester'] = np.random.choice(np.array([0, 1], dtype='float32'))
        if p['polyester'] == 1:
            p['pol_pctg'] = np.random.choice(np.array([40., 100.], dtype='float32'))
            p['cot_pcth'] = 100 - p['pol_pctg']
            if p['cot_pcth'] == 0:
                p['cotton'] = 0
            else:
                p['cotton'] = 1
        else:
            p['polyester'] = 0
            p['pol_pctg'] = 0
            p['cot_pcth'] = 100 - p['pol_pctg']
            p['cotton'] = 1
        for k, v in p.items():
            p[k] = str(v)
        data['mainProduct'] = p

    data['message'] = 'Success'
    data['scraped'] = str(scrape)
    return data


def main():
    url = 'https://www.amazon.com/Nike-drifit-Cotton-Solid-XX-Large/dp/B07DYSRT6N/'
    feat = [
        "SWEAT-WICKING NIKE T-SHIRT STYLE: The Nike Dri-FIT Men's T-Shirt delivers a soft feel, sweat-wicking performance and great range of motion to get you through your workout in total comfort.",
        "NIKE SHIRT: The Nike men's workout shirt has a standard fit for a relaxed, easy feel during physical activity. Small Nike swoosh trademark on left chest.",
        "COMFORTABLE FIT: The Nike Dry fabric material moves with you for optimal range while you play. The Nike shirt for men is crafted with 60% cotton and 40% polyester.",
        "RIBBED CREW NECK: The Nike t-shirt for men has a ribbed crew neck that gives you a comfortable fit when active. The cut is designed to lay smoothly against the skin.",
        "NIKE MEN'S SHIRT: Regular fit, fabric: 60% cotton/40% polyester, imported, machine wash"]

    prod = product.Product(url, title='Nike drift cotton Solid', color='white', price=39.47, features=feat,
                           hierarchy=['', ''], brand='', composition=['cotton', 'polyester'],
                           img='https://images-na.ssl-images-amazon.com/images/I/610fWFJNkOL._AC_SY450_.jpg',
                           scrape=False).to_dict()
    data = load_model()
    predict(data, prod)


if __name__ == "__main__":
    main()
