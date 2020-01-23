import requests
from bs4 import BeautifulSoup
from product import Product
import csv
import numpy as np
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}

URL = 'https://www.amazon.com/2UNDR-Mens-Luxury-V-Neck-X-Large/dp/B07JPB1BP1?pf_rd_p=700385e0-19d0-4b4c-89bf-06e23d6f1594&pd_rd_wg=eSwIV&pf_rd_r=VFZ0Z500YC2MQNGBJPD2&ref_=pd_gw_cr_simh&pd_rd_w=qoyy2&pd_rd_r=01e7c99b-25a4-4083-a5af-7ad97e1cf51b'
URL2 = 'https://www.amazon.com/NIKE-Legend-Short-Sleeve-White/dp/B010RRWN32/ref=sr_1_3?dchild=1&keywords=nike+white+tshirt&qid=1579702939&s=apparel&sr=1-3'
URL3 = 'https://www.amazon.com/2UNDR-Mens-Luxury-V-Neck-X-Large/dp/B07JPB1BP1?pf_rd_p=700385e0-19d0-4b4c-89bf-06e23d6f1594&pd_rd_wg=eSwIV&pf_rd_r=VFZ0Z500YC2MQNGBJPD2&ref_=pd_gw_cr_simh&pd_rd_w=qoyy2&pd_rd_r=01e7c99b-25a4-4083-a5af-7ad97e1cf51b'

START = 'https://www.amazon.com/s?k='
END = '&ref=nb_sb_noss_2'

BASE = 'https://www.amazon.com'


def create_search_url(query):
    return START + '+'.join(query.split()) + END


def scrape_search(url):
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'lxml')
    soup = soup.find('div', class_='s-result-list s-search-results sg-row')
    links_soup = soup.find_all('a', class_='a-link-normal')
    links = []
    for link in links_soup:
        if len((link['href'].split('/ref')[0] + '/').split('/')[-2]) == 10:
            links.append(link['href'].split('/ref')[0] + '/')
    links = list(set(links))
    return links


def main():
    all_links = []
    queries = ['under armour white shirt',
               'nike white shirt',
               'adidas white shirt',
               'calvin klein white shirt',
               'levis white shirt',
               'armani white shirt',
               'tommy hilfiger white shirt']
    for query in queries:
        url = create_search_url(query)
        links = scrape_search(url)
        all_links += links
    print(len(all_links))
    products = []
    for link in all_links:
        print(link)
        try:
            products.append(Product(BASE + link).to_list())
        except Exception:
            p = Product(BASE + link, title=' ', color='White', price=np.random.uniform(10, 27), features=[' '],
                        hierarchy=[' '], brand=' ',
                        composition=[' '], img=' ', scrape=False).to_list()
            products.append(p)
        print(len(products))
    with open('all_prods', 'w', newline='') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        for prod in products:
            wr.writerow(prod)


if __name__ == '__main__':
    main()
