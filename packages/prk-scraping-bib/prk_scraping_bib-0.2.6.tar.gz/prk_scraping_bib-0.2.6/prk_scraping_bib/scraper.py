import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import logging
from threading import Lock
from prk_scraping_bib.utils import get_products, get_product_links, get_categories
from prk_scraping_bib.selenium_helpers import Get_driver, accept_cookies, store_details, get_sizes

counter_lock = Lock()
counter = 0

def get_all_links(urls):
    with ThreadPoolExecutor() as executor:
        results = executor.map(get_products, urls)
        products = []
        seen_ids = set()

        for i, result in enumerate(results):
            logging.info(f"Processing sitemap {i+1}/{len(urls)}")
            for url in result:
                product_id = url.split("-")[-1]
                if product_id not in seen_ids:
                    seen_ids.add(product_id)
                    products.append(url)
    return products


def get_product(url):
    global counter
    product_dict = {'Main_category': '', 'Sub_category1': '', 'Sub_category2': '', 'product_name': '', 'price': '',
            'color_count': '', 'description': '', 'image': '', 'product_link': '','reference': ''}
    try:
        new_url,product_dict = get_product_links(url,"fr-fr",product_dict)
        r = requests.get(new_url, impersonate='chrome120')
        soup = BeautifulSoup(r.text, 'html.parser')
        product_dict['Main_category'], product_dict['Sub_category1'], product_dict['Sub_category2'] = get_categories(soup)

    except:
        try:
            new_url,product_dict = get_product_links(url,"en-us",product_dict)
            r = requests.get(new_url, impersonate='chrome120')
            soup = BeautifulSoup(r.text, 'html.parser')
            product_dict['Main_category'], product_dict['Sub_category1'], product_dict['Sub_category2'] = get_categories(soup)
        except:
            try:
                r = requests.get(url)
                soup = BeautifulSoup(r.text, 'html.parser')
                product_dict['Main_category'], product_dict['Sub_category1'], product_dict['Sub_category2'] = get_categories(soup)
                product_dict['product_link'] = url

            except:
                pass

    try:
        if r.status_code != 200:
            raise ('error statu code diffrent than 200')
        try:
            color_div = soup.find('div', {'id': "color-selector-block-gallery"}).find_all('a')
            color_count = len(color_div)
            product_dict['color_count'] = color_count

        except:
            product_dict['color_count'] = 0
        price = soup.find('p', class_='MuiTypography-root MuiTypography-body1 HeaderAndPrice-price css-g9ki7z').text
        product_dict['price'] = price
        product_name = soup.find('h1').text
        divs = soup.find('div', class_="MuiAccordionDetails-root ProductDetailsAccordeonSection-details css-vbq0r2")
        description = divs.text
        product_dict['product_name'] = product_name
        product_dict['description'] = description.replace("\n", " / ")
        image = soup.find('img', class_="ProductGallery-productImage")
        product_dict['image'] = image['srcset']
        product_dict['reference'] = url.split("-")[-1]
        with counter_lock:
            counter += 1
            logging.info(f'Processed {counter} products')

        return product_dict
    except:
        with counter_lock:
            counter += 1
            logging.info(f'Processed {counter} products')
        return product_dict