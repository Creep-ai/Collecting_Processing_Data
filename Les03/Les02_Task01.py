from bs4 import BeautifulSoup as bs
import requests
import re
from pprint import pprint
import hashlib


def parser_hh(soup):
    main_link_hh = 'https://hh.ru'
    vacancies_page_list = []
    # находим блок со списком вакансий
    vacancies_block = soup.find('div', {'class': 'vacancy-serp'})
    # получаем список вакансий
    vacancies_list = vacancies_block.findChildren('div', {'class': 'vacancy-serp-item'}, recursive=False)
    # вытаскиваем необходимые сведения по вакансии:
    for vacancy in vacancies_list:
        vacancy_data = {}
        vacancy_name = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).text
        salary = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).text
        vacancy_link = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href']
        if len(salary) == 0:
            min_salary, max_salary = float('nan'), float('nan')
            currency = [float('nan')]
        else:
            currency = re.search('([^\d]*$)', salary)
            _sal = salary.split('-')
            if len(_sal) == 1:
                if 'от' in _sal[0]:
                    min_salary = re.sub('\D', '', _sal[0])
                    max_salary = float('nan')
                else:
                    max_salary = re.sub('\D', '', _sal[0])
                    min_salary = float('nan')
            else:
                min_salary = re.sub('\D', '', _sal[0])
                max_salary = re.sub('\D', '', _sal[1])
        vacancy_data['name'] = vacancy_name
        vacancy_data['min_salary'] = min_salary
        vacancy_data['max_salary'] = max_salary
        vacancy_data['link'] = vacancy_link
        vacancy_data['source'] = main_link_hh
        vacancy_data['cur'] = currency[0]
        hash_str = f'{vacancy_link}{str(min_salary)}{str(max_salary)}'
        vacancy_data['hash'] = hashlib.md5(bytes(hash_str, 'utf-8')).hexdigest()
        vacancies_page_list.append(vacancy_data)
    return vacancies_page_list


def parser_sj(soup):
    main_link_sj = 'https://russia.superjob.ru'
    vacancies_page_list = []
    # находим блок со списком вакансий
    vacancies_block = soup.find('div', {'class': '_1ID8B'})
    # получаем список вакансий
    vacancies_list = vacancies_block.findChildren('div', {'class': '_1fMKr'})
    # вытаскиваем необходимые сведения по вакансии:
    for vacancy in vacancies_list:
        vacancy_data = {}
        if vacancy.find('span', {'class': '_1rS-s'}) is not None:
            vacancy_name = vacancy.find('a', {'class': 'icMQ_'}).text
            vacancy_link = main_link_sj + vacancy.find('a', {'class': 'icMQ_'})['href']
            salary = vacancy.find('span', {'class': 'f-test-text-company-item-salary'}).text
            salary.replace(' ', '')
            if salary == 'По договорённости':
                min_salary, max_salary = float('nan'), float('nan')
                currency = [float('nan')]
            else:
                currency = re.search('([^ ]*$)', salary)
                _sal = salary.split('—')
                if len(_sal) == 1:
                    if 'от' in _sal[0]:
                        min_salary = float(re.sub('\D', '', _sal[0]))
                        max_salary = float('nan')
                    else:
                        max_salary = float(re.sub('\D', '', _sal[0]))
                        min_salary = float('nan')
                else:
                    min_salary = float(re.sub('\D', '', _sal[0]))
                    max_salary = float(re.sub('\D', '', _sal[1]))
            vacancy_data['min_salary'] = min_salary
            vacancy_data['max_salary'] = max_salary
            vacancy_data['name'] = vacancy_name
            vacancy_data['cur'] = currency[0]
            vacancy_data['source'] = main_link_sj
            vacancy_data['link'] = vacancy_link
            hash_str = f'{vacancy_link}{str(min_salary)}{str(max_salary)}'
            vacancy_data['hash'] = hashlib.md5(bytes(hash_str, 'utf-8')).hexdigest()
            vacancies_page_list.append(vacancy_data)
    return vacancies_page_list


def search_vacancies():
    page_count = int(input('Введите кол-во страниц для парсинга: '))
    user_vacancy_name = input('Введите название интересующей вакансии: ')

    main_link_sj = 'https://russia.superjob.ru'
    main_link_hh = 'https://hh.ru'

    params_sj = {'keywords': user_vacancy_name}
    params_hh = {'clusters=true': 'serials',
                 'enable_snippets': 'true',
                 'text': user_vacancy_name,
                 'L_save_area': 'true',
                 'area': '113',
                 'from': 'cluster_area',
                 'showClusters': 'true',
                 'customDomain': '1'}

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/83.0.4103.61 Safari/537.36'}

    vacancies = []

    # Парсим hh.ru
    i = 1
    response_hh = requests.get(main_link_hh + '/search/vacancy', params=params_hh, headers=headers)
    soup = bs(response_hh.text, 'lxml')
    vacancies = vacancies + parser_hh(soup)

    # находим блок с кнопкой "далее"
    pager_block = soup.find('div', {'data-qa': 'pager-block'})
    next_page_link = pager_block.find('a', {'class': 'HH-Pager-Controls-Next'})

    while i < page_count and (next_page_link is not None):
        link = main_link_hh + next_page_link['href']
        response_hh = requests.get(link, headers=headers)
        soup = bs(response_hh.text, 'lxml')
        vacancies = vacancies + parser_hh(soup)
        # находим блок с кнопкой "далее"
        pager_block = soup.find('div', {'data-qa': 'pager-block'})
        next_page_link = pager_block.find('a', {'class': 'HH-Pager-Controls-Next'})
        i += 1

    # Парсим SuperJob.ru
    j = 1
    response_sj = requests.get(main_link_sj + '/vacancy/search', params=params_sj, headers=headers)
    soup = bs(response_sj.text, 'lxml')
    vacancies = vacancies + parser_sj(soup)

    # находим блок с кнопкой "далее"
    pager_block = soup.find('div', {'class': 'L1p51'})
    next_page_link = pager_block.find('a', {'class': 'f-test-link-Dalshe'})
    # pprint(next_page_link['href'])

    while j <= page_count and (next_page_link is not None):
        link = main_link_sj + next_page_link['href']
        response_sj = requests.get(link, headers=headers)
        soup = bs(response_sj.text, 'lxml')
        vacancies = vacancies + parser_sj(soup)
        # находим блок с кнопкой "далее"
        pager_block = soup.find('div', {'class': 'L1p51'})
        next_page_link = pager_block.find('a', {'class': 'f-test-link-Dalshe'})
        # pprint(next_page_link['href'])
        j += 1

    # pprint(vacancies)
    print(f'Найдено {len(vacancies)} вакансий')
    return vacancies
#
#
# x = search_vacancies()
# pprint(x)
# result = search_vacancies()