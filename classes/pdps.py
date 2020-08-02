import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from flask import jsonify
from helper import *

class PDP():
    def __init__(self, master, info):
        self.master = master
        self.url = self.add_url(info)
        self.status = ''
        self.title = ''
        self.wwmt = ''
        self.fivef = ''
        self.bread = ''
        self.color = ''
        self.price = ''
        self.size = ''
        self.img_count = '' 


    def add_url(self, info):
        site = info['site']
        siteEnv = info['siteEnv']
        date = info['date']
        
        domain = site_selector(site, siteEnv) + '/p/dummy/'
        
        if len(date) == 0:
            self.url = domain + self.master + '.html'
        else:
            date_s = parsedate(date)
            self.url = domain + self.master + '.html?__siteDate=' + date_s
        return self.url
    

    def fill_in(self, s, info):
        email = info['email']
        password = info['password']
        url = self.url

        response = s.get(url, auth=HTTPBasicAuth(email, password))
        self.status = response.status_code

        if self.status != 200:
            return self

        soup = BeautifulSoup(response.text,'html.parser')
        # Title
        self.title = soup.find(class_='product-name d-none d-lg-block').text
        # WWMT
        wwmt = soup.find(class_='product-message').text.strip()
        self.wwmt = wwmt.replace('\n', '')
        # 5Fs
        f = soup.find(
            class_='additional-description-and-detail').text.strip()
        self.fivef = " ".join(f.split())
        # Breadcrumb
        crumb = soup.find_all(class_='breadcrumb-item')
        b = []
        for c in crumb:
            b.append(c.text.strip())
        self.bread = " > ".join(b)
        # Color
        if soup.find(class_='selected-swatch-name') == None:
            self.color = ''
        else:
            self.color = soup.find(class_='selected-swatch-name').text
        # Price
        prices = soup.find_all(class_='value')
        price = []
        for p in prices:
            price.append(p.text.strip())
        price = list(set(price))
        self.price = " - ".join(price)
        # Sizes
        sizes = soup.find_all('option', {'id': 'sizeSelected'})
        size = []
        for s in sizes:
            size.append(s.text.strip())
        self.size = ", ".join(size)
        # Image count
        self.img_count = len(soup.find_all(class_='carousel-item-message'))
        
        return self


    @property
    def print_full(self):
        return {'master': self.master, 'url': self.url, 'status': self.status, 'title': self.title, 'wwmt': self.wwmt,
        'fivef': self.fivef, 'bread': self.bread, 'color': self.color, 'price': self.price, 'size': self.size,
        'img_count': self.img_count}

def pdpscraper(styles, info):
    s = requests.Session()
    
    results = [] 

    for style in styles:
        style.fill_in(s, info)
        content = style.print_full
        results.append(content)
    
    return results