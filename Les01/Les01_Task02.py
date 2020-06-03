# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import json
from pprint import pprint

import requests
import random

lat = random.uniform(-90, 90)
lon = random.uniform(-180, 180)

link = 'https://api.geoapify.com/v1/geocode/reverse?lat=' + str(lat) + '&lon=' + str(lon) + '&apiKey=6caca1e7e6e54074ba58af26db675b61'

req = requests.get(link)

data = req.json()
pprint(data)
print(f'Мы попали в {data["properties"]["datasource"]["name"]}')
with open('Les01_Task02.json', 'w') as f:
    json.dump(data, f)

with open('Les01_Task02.json', 'r') as f:
    result = json.load(f)
    print(f'Мы попали в {result["features"][0]["properties"]["name"]}')

print('ok')
