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
            data["title"] != " ")].sort_values(
        by="ecoscore", ascending=False)[:3].set_index(pd.Index(["firstSuggestion", "secondSuggestion", "thirdSuggestion"]))

    # final_df = pd.concat([new_df, data])

    data = data.to_dict(orient="index")
    data['mainProduct'] = {'title': dct['title'], 'brand': dct['brand'], 'price': dct['price'],
                           'description': ' '.join(dct['features']), 'brand_score': 3, 'cotton': 1, 'cot_pcth': 60.,
                           'polyester': 1, 'pol_pctg': 40., 'ismale': 1, 'urlPhoto': dct['photoUrl'], 'weight': 0.157,
                           'co2': 4.47,
                           'ecoscore': 4.32}
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
