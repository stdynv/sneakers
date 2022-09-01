from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(executable_path='C://Users//Yassine//Downloads//chromedriver.exe')
driver.maximize_window()
WebDriverWait(driver, 10)
driver.get('https://www.nike.com/fr/w/mixte-chaussures-3rauvzy7ok')

WebDriverWait(driver, 15)

global product_name, product_prices, product_availableColors, product_desc
# product_name = list()
# disable tracking
# product_name = list()
reject_cookies = driver.find_element(By.XPATH, '//button[@data-var="rejectBtn"]').click()
for x in range(1, 16):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    WebDriverWait(driver, 5)
    scrap_name = driver.find_elements(By.CSS_SELECTOR, '.product-card__title')
    product_name = [name.text for name in scrap_name]
    WebDriverWait(driver, 5)
    scrap_description = driver.find_elements(By.CSS_SELECTOR, '.product-card__subtitle')
    product_desc = [desc.text for desc in scrap_description]
    WebDriverWait(driver, 5)
    scrap_price = driver.find_elements(By.CSS_SELECTOR, 'div.product-price.is--current-price')
    product_prices = [price.text for price in scrap_price]
    WebDriverWait(driver, 5)
    scrap_colors = driver.find_elements(By.CSS_SELECTOR, '.product-card__product-count')
    product_availableColors = [color.text for color in scrap_colors]

    print(len(product_desc))

nike_csv = {
    'product Name': product_name,
    'Product Description': product_desc,
    'Price': product_prices,
    'Colors Available': product_availableColors,
    'Sex': 'Unisex'

}

df = pd.DataFrame(nike_csv)
df.to_csv('nike_mixte.csv')
