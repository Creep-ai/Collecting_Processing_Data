# Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
# Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары

import time
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Firefox()
driver.maximize_window()
driver.get('https://mvideo.ru/')

button = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.CLASS_NAME, 'btn-approve-city'))
)
button.click()

time.sleep(5)
driver.get(driver.current_url)
driver.execute_script('window.scrollTo(0, 2000)')
time.sleep(5)
buttons = driver.find_elements_by_xpath('//a[@class="next-btn sel-hits-button-next"]')

for i in range(5):
        buttons[1].click()
        time.sleep(2)

elems = driver.find_elements_by_class_name('sel-hits-block')
product_blocks = elems[1].find_elements_by_xpath('.//li')
list_to_export = []

for block in product_blocks:
    product_dict = {}
    title = block.find_element_by_class_name('sel-product-tile-title')
    price = block.find_element_by_class_name('c-pdp-price__current')
    product_dict['title'] = title.text
    product_dict['price'] = price.text
    list_to_export.append(product_dict)

print(list_to_export)

client = MongoClient('localhost', 27017)
db = client['mvideo']
mvideo = db.mvideo
# mvideo.delete_many({})
mvideo.insert_many(list_to_export)
print('done')
