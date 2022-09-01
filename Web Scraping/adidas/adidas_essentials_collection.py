import random
from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType

driver = webdriver.Chrome(executable_path='C://Users//Yassine//Downloads//chromedriver.exe')
driver.maximize_window()

WebDriverWait(driver, 10)
sex = list()
all_product_name = list()
all_product_prices = list()
all_product_collection = list()
all_product_color_number = list()

page = 0
current_page = 1
page_cheat = 0

while page <=  3792:
    driver.get(f'https://www.adidas.fr/chaussures?start={page}')
    # enable cookies for scraping
    WebDriverWait(driver,10)
    if page == 0:
        cookies_reject = driver.find_element(By.XPATH, '//button[@data-auto-id="glass-gdpr-default-consent-reject-button"]')
        cookies_reject.click()
    page_cheat+= 1
    page = page + 48
    WebDriverWait(driver, 10)

    links = driver.find_elements(By.CSS_SELECTOR, '.grid-item a.glass-product-card__assets-link')
    all_shoes = [link.get_attribute('href') for link in links]
    for shoes in all_shoes:
        WebDriverWait(driver,30)
        driver.get(shoes)
        # get title
        scrap_product_name = driver.find_element(By.XPATH, '//h1[@data-auto-id="product-title"]/span').get_attribute("textContent")
        all_product_name.append(scrap_product_name)
        # price
        scrap_price_product = driver.find_element(By.CLASS_NAME, 'gl-price-item.notranslate').get_attribute(
            "textContent")
        all_product_prices.append(scrap_price_product)
        # collection
        try:
            scrap_col_product = driver.find_element(By.XPATH, '//div[@data-auto-id="product-category"]/span').get_attribute('textContent')
            all_product_collection.append(scrap_col_product)
        except :
            all_product_collection.append('Uknown')
        # number of colors availables
        try :

            scrap_color_product = driver.find_element(By.XPATH, '//div[@class="available-colors-label--sticky___3NXOG"]').get_attribute('textContent')
            all_product_color_number.append(scrap_color_product)
        except :
            all_product_color_number.append('1 Coloris disponibles')
    print(current_page)
    current_page += 1

driver.close()
adidas_csv = {
    'product_name': all_product_name,
    'product price': all_product_prices,
    'Collection': all_product_collection,
    'Colors Available' : all_product_color_number
}

df = pd.DataFrame(adidas_csv)
pos = 0

for s in df.Collection :
    if '•' in s :
        sex.append(s[0:s.index('•')])
        df.loc[pos, 'Collection'] = s[s.index('•') + 1::].strip()

    else :
        sex.append('Unisex')
    pos +=1

df['Sex'] = sex
df.to_csv('adidas_product_18_80.csv')
