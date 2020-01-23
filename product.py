import requests
from bs4 import BeautifulSoup
import numpy as np

MATERIALS = ['cotton', 'spandex', 'poly', 'modal']
MATERIALS_DICT = {'poly': 'polyester'}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


class Product:
    def __init__(self, url, title=None, color=None, price=None, features=None, hierarchy=None, brand=None,
                 composition=None, img=None, scrape=True):
        if composition is None:
            composition = []
        s = requests.session()
        s.cookies.clear()
        resp = requests.get(url, headers=headers)
        self.url = url
        self.soup = BeautifulSoup(resp.text, 'lxml')
        self.brand = brand
        self.title = title
        self.color = color
        self.price = price
        self.features = features
        self.hierarchy = hierarchy
        self.composition = composition
        self.img = img
        self.ecoscore = np.random.choice(np.arange(1, 11))
        self.scrape = scrape
        if scrape:
            self.__center_col()
            self.__wayfinding()
            self.__parse_price()
            if not self.composition:
                self.__get_composition()
            self.__get_image()

    def __parse_price(self):
        price = self.price.split('-')
        if len(price) == 1:
            self.price = float(price[0].replace('$', ''))
        else:
            self.price = round(sum([float(p.replace('$', '')) for p in price]) / 2, 2)

    @staticmethod
    def clean_text(text):
        return text.replace('\n', '').replace('\t', '').strip()

    def __center_col(self):
        soup = self.soup.find('div', id='centerCol')
        try:
            price = soup.find('div', id='desktop_unifiedPrice')
            self.price = price.find('span', id="priceblock_ourprice").text
        except Exception:
            self.price = np.random.uniform(10, 25)
        # self.price = price.find('span', id="priceblock_ourprice").text
        bullets_html = soup.find('div', id='feature-bullets')
        bullets_html = bullets_html.find_all('span', class_='a-list-item')
        bullets = []
        for bullet in bullets_html:
            bullets.append(bullet.text.strip())
        self.features = bullets
        color = soup.find('div', id='variation_color_name')
        self.color = color.find('span', class_='selection').text.strip()
        self.title = soup.find('span', id='productTitle').text.strip()
        try:
            self.brand = soup.find('a', id='brand')['href'].split('/')[1]
        except Exception:
            self.brand = self.title.split()[0]

    def __wayfinding(self):
        crums = self.soup.find('div', id='wayfinding-breadcrumbs_container')
        crums = crums.find_all('span', class_='a-list-item')
        product_classes = []
        for crum in crums:
            try:
                product_classes.append(crum.find('a').text.strip())
            except Exception:
                pass
        self.hierarchy = product_classes

    def __get_composition(self):
        for feature in self.features:
            for material in MATERIALS:
                if material in feature.lower():
                    if material in MATERIALS_DICT:
                        self.composition.append(MATERIALS_DICT[material])
                    else:
                        self.composition.append(material)
        self.composition = list(set(self.composition))

    def __get_image(self):
        soup = self.soup.find('div', id="main-image-container")
        self.img = soup.find('img', id='landingImage')['data-a-dynamic-image'].split('"')[1]

    def to_dict(self):
        d = {}
        d['brand'] = self.brand
        d['title'] = self.title
        d['composition'] = self.composition
        d['type'] = self.hierarchy[-1]
        d['parent_type'] = self.hierarchy[-2]
        d['price'] = self.price
        d['features'] = self.features
        d['ecoscore'] = self.ecoscore
        d['photoUrl'] = self.img
        d['url'] = self.url
        return d

    def to_list(self):
        l = []
        l.append(self.title)
        l.append(self.brand)
        l.append(self.price)
        l.append(' '.join(self.features))
        l.append(self.ecoscore)
        l.append(' '.join(self.composition))
        l.append(' '.join(self.hierarchy))
        l.append(self.img)
        l.append(self.url)
        return l
