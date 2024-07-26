import requests
from bs4 import BeautifulSoup



def get_product_links(url,country_tag,product_dict):
    url_country = url.split("/")[-3]
    new_url = url.replace(url_country,country_tag)
    product_dict['product_link'] = new_url
    return new_url,product_dict

def get_categories(soup):    
    ol_selector = soup.find('ol', class_="MuiBreadcrumbs-ol css-nhb8h9")
    category = ol_selector.text.split("/")
    return category[0], category[1], category[2]

def get_products(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    urls = soup.find_all('loc')
    links = [url.text for url in urls]
    return links
