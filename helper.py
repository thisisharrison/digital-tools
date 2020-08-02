from bs4 import BeautifulSoup
from flask import jsonify
import requests
from requests.auth import HTTPBasicAuth

def query_edit(query):
    
    # modify search to same format and split into list 
    query = query.replace('\t', '\r\n')
    query = query.replace(' ', '\r\n')
    query = query.replace(',', '\r\n')
    queryset = query.split('\r\n')

    # get unique values and remove blanks
    queryset = list(set(queryset))
    for i in range(len(queryset)-1):
        if len(queryset[i]) == 0:
            queryset.pop(i)

    return queryset



def url_edit(url, date=''):
    if len(date) > 0:
        date_s = parsedate(date)
    
    if '?' in url:
        idx = url.find('?')
        url = url[0:idx]

    if len(date) > 0:
        url = url + '?__siteDate=' + date_s + '&sz=9999'
    else:
        url = url + '?sz=9999'

    return url


def cdp_scrape(url, info):
    email = info['email']
    password = info['password']
    date = info['date']
    siteEnv = info['siteEnv']

    url = url_edit(url, date)

    s = requests.Session()
    response = s.get(url, auth=HTTPBasicAuth(email, password))

    prefix = url_prefix(url, siteEnv)
    print(prefix)

    if response.status_code != 200:
        return jsonify ({'success': False})
    else: 
        soup = BeautifulSoup(response.text, "html.parser")
        pdps = soup.find_all(class_="pdp-link")
        result = []
        for pdp in pdps:
            a = pdp.find("a")

            href = a.get("href")
            href = prefix + href

            char = href.split("/")
            char0 = char[len(char)-1].split(".")
            master = char0[0]

            title = a.text.strip()

            product = {"master": master,
                       "link": href, "title": title}
            result.append(product)
        return(result)

def site_selector(site, siteEnv=''):
    # siteEnv = 'staging' / 'production'

    production = {
        'HK': 'https://www.lululemon.com.hk/en-hk',
        'JP': 'https://www.lululemon.co.jp/ja-jp',
        'AU': 'https://www.lululemon.com.au/en-au',
        'UK': 'https://www.lululemon.co.uk/en-gb',
        'EU': 'https://www.eu.lululemon.com/en-lu',
        'FR': 'https://www.lululemon.fr/fr-fr',
        'DE': 'https://www.lululemon.de/de-de'
    }

    staging = {
        'HK': 'https://staging-eu01-lululemon.demandware.net/s/HK/en-hk',
        'JP': 'https://staging-eu01-lululemon.demandware.net/s/JP/ja-jp',
        'AU': 'https://staging-eu01-lululemon.demandware.net/s/AU/en-au',
        'UK': 'https://staging-eu01-lululemon.demandware.net/s/UK/en-gb',
        'EU': 'https://staging-eu01-lululemon.demandware.net/s/EU/en-lu',
        'FR': 'https://staging-eu01-lululemon.demandware.net/s/FR/fr-fr',
        'DE': 'https://staging-eu01-lululemon.demandware.net/s/DE/de-de'
    }

        # Eg. 'https://staging-eu01-lululemon.demandware.net/s/HK/en-hk/p/adapt-to-you-tank/LW1CQ3S.html?__siteDate=20200811'

    if siteEnv == 'production' or siteEnv == '':
        for country, domain in production.items():
            if site in domain or site in country:
                return domain
    elif siteEnv == 'staging':
        for country, domain in staging.items():
            if site in domain or site in country:
                return domain

    


def url_prefix(url, siteEnv):
    parts = url.split('/')
    if siteEnv == 'staging':
        for part in parts:
            if len(part) == 2:
                return site_selector(part, siteEnv)
    else:
        return site_selector(parts[2], siteEnv)
    
        
    
def parsedate(string):
    # Eg. '2020-08-02'
    if not '-' in string:
        return ''
    else:
        return string.replace('-','')