# My Scraper

A Python library for scraping product details and availability from e-commerce websites.

Functions
checking_status(url)
Description: Checks the HTTP status code of a given URL.
Parameters: url (str) - The URL to check.
Returns: The URL if the status code is 200, otherwise None.
get_product_links(url, country_tag, dict)
Description: Retrieves product links and updates the dictionary with the new URL.
Parameters:
url (str) - The original URL.
country_tag (str) - The country code to replace in the URL.
dict (dict) - The dictionary to update with the new URL.
Returns: A tuple containing the BeautifulSoup object and the updated dictionary.
Get_driver(link)
Description: Initializes and returns a Selenium WebDriver.
Parameters: link (str) - The URL to navigate to.
Returns: Selenium WebDriver instance.
accept_cookies(driver)
Description: Accepts cookies on the webpage if the button is present.
Parameters: driver (WebDriver) - The Selenium WebDriver instance.
Returns: None
store_details(driver, dict_details, size_name)
Description: Extracts store details (name, address, availability) and updates the dictionary.
Parameters:
driver (WebDriver) - The Selenium WebDriver instance.
dict_details (dict) - The dictionary to update with store details.
size_name (str) - The size category to update in the dictionary.
Returns: Updated dictionary with store details.
get_categories(soup)
Description: Extracts product categories from a BeautifulSoup object.
Parameters: soup (BeautifulSoup) - The BeautifulSoup object containing the page content.
Returns: A tuple containing the main category, subcategory1, and subcategory2.
get_products(url)
Description: Retrieves product links from a sitemap URL.
Parameters: url (str) - The sitemap URL.
Returns: A list of product links.
get_sizes(link)
Description: Scrapes sizes and availability details for a product.
Parameters: link (str) - The product URL.
Returns: A dictionary with size and availability details.
get_product(url)
Description: Retrieves detailed product information from the given URL.
Parameters: url (str) - The product URL.
Returns: A dictionary containing product details (categories, name, price, description, image, etc.).