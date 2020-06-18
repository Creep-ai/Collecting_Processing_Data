# Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о
# письмах в базу данных:
# * от кого,
# * дата отправки,
# * тема письма,
# * текст письма полный
import datetime
import time

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

fox_options = Options()

# fox_options.add_argument('--start-maximized')
# fox_options.add_argument('-headless')

driver = webdriver.Firefox(options=fox_options)
driver.maximize_window()
driver.get('https://mail.ru/')

elem = driver.find_element_by_id('mailbox:login')
elem.send_keys('<insert_login>')
elem.send_keys(Keys.RETURN)

time.sleep(2)
elem = driver.find_element_by_id('mailbox:password')
elem.send_keys('<insert_password>')
elem.send_keys(Keys.RETURN)

elem = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'llc'))
)

driver.get(elem.get_attribute('href'))

total_list = []

while True:
    dict_mail = {}
    # print(driver.current_url)
    driver.get(driver.current_url)
    author = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'letter-contact'))
    )
    date = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'letter__date'))
    )
    subject = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'thread__subject'))
    )
    body = driver.find_element_by_class_name('letter-body__body-content')
    if 'Сегодня' in date.text:
        date_corrected = f'{datetime.date.today()} {date.text[-5:]}'
        dict_mail['date'] = date_corrected
    else:
        dict_mail['date'] = date.text
    dict_mail['content'] = body.text
    dict_mail['author'] = author.text
    dict_mail['subject'] = subject.text
    # print(dict_mail)
    total_list.append(dict_mail)
    next_mail = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'portal-menu-element_next'))
    )
    if EC.element_to_be_clickable((By.CLASS_NAME, 'portal-menu-element_next')) == False:
        break
    next_mail.click()
print('Collecting e-mails...\nPlease wait...')

client = MongoClient('localhost', 27017)
db = client['mailru']
mailru = db.mailru
# mailru.delete_many({})
mailru.insert_many(total_list)
print('done')
