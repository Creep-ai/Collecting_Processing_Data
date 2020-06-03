# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

from pprint import pprint

import json
import requests

req = requests.get('https://api.github.com/users/Creep-ai/repos?per_page=100')

data = req.json()

with open('Les01_Task01.json', 'w') as f:
    json.dump(data, f)

with open('Les01_Task01.json', 'r') as f:
    result = json.load(f)

# pprint(result)

print('ok!')
