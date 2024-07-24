import requests
from bs4 import BeautifulSoup

def get_sitemaps(filepath):
    with open(filepath) as f:
        urls = f.read().splitlines()
    return urls

def get_product_links(url, country_tag, product_dict):
    url_country = url.split("/")[-3]
    new_url = url.replace(url_country, country_tag)
    product_dict['product_link'] = new_url
    return new_url, product_dict

def get_categories(soup,categories_class):
    ol_selector = soup.find('ol', class_=categories_class)
    category = ol_selector.text.split("/")
    return category[0], category[1], category[2]

def get_products(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = soup.find_all('loc')
    links = [url.text for url in urls]
    return links
