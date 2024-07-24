from pathlib import Path
import sys
import os
current_directory = Path(__file__).parent.absolute()
root_path = current_directory.parent
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(str(root_path))


import unittest
from prk_scraping_bib.scraper import get_all_links, get_product, get_sizes

class TestScraper(unittest.TestCase):
   # def test_get_sitemaps(self):
    #    urls = get_sitemaps("site_maps.txt")
     #   self.assertTrue(len(urls) > 0)

   # def test_get_all_links(self):
    #    urls = get_sitemaps("site_maps.txt")
     #   products = get_all_links(urls)
      #  self.assertTrue(len(products) > 0)

    def test_get_product(self):
        product_url = "https://www.primark.com/en-gb/p/multi-compartment-weekend-bag-black-991100076804"
        details = get_product(product_url)
        self.assertIn('product_name', details)

    def test_get_sizes(self):
        product_url = "https://www.primark.com/en-gb/p/multi-compartment-weekend-bag-black-991100076804"
        sizes = get_sizes(product_url)
        self.assertIsInstance(sizes, dict)

if __name__ == '__main__':
    unittest.main()