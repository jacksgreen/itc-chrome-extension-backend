import requests
# from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np


def load_model():
    return pd.read_excel("data.xlsx")


def predict(data, dct):

    cols = ["Title", "Brand", "Price", "Description", "brand_score", "cotton", "cot_pctg", "polyester", "pol_pctg",
            "ismale", "urlPhoto", "url", "weight", "co2", "ecoscore"]

    #new_df = pd.DataFrame.from_dict(dct, orient='index')
    #return new_df.to_dict(orient="index")
    data = data[(data["Price"] > 0.8 * dct["price"]) & (data["Price"] < 1.2 * dct["price"]) & (data["Title"] != " ")].sort_values(by="ecoscore", ascending=False)[:3].set_index(pd.Index(["first_rec", "second_rec", "third_rec"]))

    #final_df = pd.concat([new_df, data])

    return data.to_dict(orient="index")


def main():
    data = load_model()
    predict(data, X_test)


if __name__ == "__main__":
    main()
