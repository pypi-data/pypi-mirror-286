from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def Get_driver(link):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get(link)
    return driver

def accept_cookies(driver,ID_name):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,ID_name))).click()
    except:
        pass


def store_details(driver, dict_details, size_name):
    store_names = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="StoreCard-storeInfo MuiBox-root css-0"]/div/h5')))[:5]
    store_addresses = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="StoreCard-storeInfo MuiBox-root css-0"]/p')))[:5]
    store_availability = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="StoreCard-status MuiBox-root css-0"]/p')))[0::2][:5]
    dict2 = {}
    for store_name, store_address, store_available in zip(store_names, store_addresses, store_availability):
        dict2["store_name"] = store_name.text
        dict2["store_address"] = store_address.text
        dict2["store_available"] = store_available.text
        dict_details[size_name].append(dict2)
    return dict_details

def get_sizes(link):
    driver = Get_driver(link)
    dict = {}
    dict["link"] = link
    accept_cookies(driver,"onetrust-accept-btn-handler")
    placeholder_content= "NONE"
    try:
        input_element = input_element = driver.find_element(By.CLASS_NAME,"MuiSelect-nativeInput")
        placeholder_content = input_element.get_attribute("placeholder")
    except:
        pass
    if placeholder_content != "NONE":
        #sizes list button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="mui-2"]'))).click()
        sizes = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//li[@class="MuiButtonBase-root MuiMenuItem-root MuiMenuItem-gutters MuiMenuItem-root MuiMenuItem-gutters css-19fafqr"]')))
        action_chains = ActionChains(driver)
        for i in range(len(sizes)):
            size = sizes[i]
            size_name = size.text
            driver.execute_script("arguments[0].scrollIntoView();", size)
            action_chains.move_to_element(size).perform()
            size.click()
            dict[size_name] = []
            check_availability_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="MuiButtonBase-root MuiButton-root MuiButton-outlined MuiButton-outlinedPrimary MuiButton-sizeLarge MuiButton-outlinedSizeLarge MuiButton-colorPrimary MuiButton-disableElevation MuiButton-root MuiButton-outlined MuiButton-outlinedPrimary MuiButton-sizeLarge MuiButton-outlinedSizeLarge MuiButton-colorPrimary MuiButton-disableElevation SalesPanel-block SalesPanel-checkAvailabilityBox css-q985dj"]')))
            check_availability_button.click()
            dict = store_details(driver, dict, size_name)
            close_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="MuiButtonBase-root MuiIconButton-root MuiIconButton-colorInherit MuiIconButton-sizeLarge StoreSelectorContent-closeButton css-m8q4ei"]')))
            close_button.click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="mui-2"]'))).click()
            sizes = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//li[@class="MuiButtonBase-root MuiMenuItem-root MuiMenuItem-gutters MuiMenuItem-root MuiMenuItem-gutters css-19fafqr"]')))
    else:
        size_name = '1 size'
        dict[size_name] = []
        check_availability_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="MuiButtonBase-root MuiButton-root MuiButton-outlined MuiButton-outlinedPrimary MuiButton-sizeLarge MuiButton-outlinedSizeLarge MuiButton-colorPrimary MuiButton-disableElevation MuiButton-root MuiButton-outlined MuiButton-outlinedPrimary MuiButton-sizeLarge MuiButton-outlinedSizeLarge MuiButton-colorPrimary MuiButton-disableElevation SalesPanel-block SalesPanel-checkAvailabilityBox css-q985dj"]')))
        check_availability_button.click()
        dict = store_details(driver, dict, size_name)
    driver.quit()
    return dict
