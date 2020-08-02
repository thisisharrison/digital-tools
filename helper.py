from bs4 import BeautifulSoup
from flask import jsonify
import requests

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



def url_edit(url):
    if '?sz=' in url:
        idx = url.find('?sz=') + 4
        url = url [0:idx] + '9999'
    elif '?icid' in url:
        url = url + '&sz=9999'
    elif url[-1] != '/':
        url = url+'/?sz=9999'
    else:
        url = url+'?sz=9999'
    return url 



def cdp_scrape(url):
    s = requests.Session()
    response = s.get(url)

    prefix = url_prefix(url)

    if response.status_code != 200:
        return jsonify ({'success': False})
    else: 
        url = url_edit(url)
        response = s.get(url)
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

def site_selector(site, siteEnv):
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
        'JP': 'https://staging-eu01-lululemon.demandware.net/s/JP/ja-jp/',
        'AU': 'https://staging-eu01-lululemon.demandware.net/s/AU/en-au/'
    }

# 'https://staging-eu01-lululemon.demandware.net/s/HK/en-hk/p/adapt-to-you-tank/LW1CQ3S.html?__siteDate=20200811'

    if siteEnv == 'production':
        for country, domain in production.items():
            if site in domain or site in country:
                return domain
    elif siteEnv == 'staging':
        for country, domain in staging.items():
            if site in domain or site in country:
                return domain

    


def url_prefix(url):
    partial_prefix = url.split('-')[0]
    print (partial_prefix)
    return site_selector(partial_prefix)
    
def parsedate(string):
    # Eg. '2020-08-02'
    return string.replace('-','')