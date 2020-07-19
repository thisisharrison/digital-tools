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
    if url[-1].isnumeric():
            parts = query.split("?sz=")
            url = parts[0]+'?sz=9999'
    elif url[-1] != '/':
        url = url+'/?sz=9999'
    else:
        url = url+'?sz=9999'
    return url 

def cdp_scrape(url):
    s = requests.Session()
    response = s.get(url)
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
            hk_prefix = "https://www.lululemon.com.hk/en-hk/p/lab-kosaten-pant/"
            href = hk_prefix+href

            char = href.split("/")
            char0 = char[len(char)-1].split(".")
            master = char0[0]

            title = a.text.strip()

            product = {"master": master,
                       "link": href, "title": title}
            result.append(product)
        return(result)



