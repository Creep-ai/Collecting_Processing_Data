from pymongo import MongoClient
from Les03.Les02_Task01 import *
from pprint import pprint


client = MongoClient('localhost', 27017)
db = client['vacancies']
vacancies = db.vacancies


def no_doubles(vacancies):
    result = search_vacancies()
    count_new = 0
    count_upd = 0
    for i in range(len(result)):
        # в функциях парсинга создал ключ 'hash', который хэширует с помощью md5 строку, сложенную из ссылки на
        # вакансию, мин и макс зп. Таким образом, в случае обновления зп на существующую вакансию, это можно будет
        # отследить простым запросом:
        if vacancies.count_documents({'hash': result[i]['hash']}) != 0:
            continue
        elif vacancies.count_documents({'link': result[i]['link']}) != 0:
            # vacancies.update({'link': result[i]['link']},
            #                  {'min_salary': result[i]['min_salary'], 'max_salary': result[i]['max_salary'],
            #                   'hash': result[i]['hash']})
            vacancies.update_one({'link': result[i]['link']}, {'$set': result[i]})
            count_upd += 1
        elif vacancies.count_documents({'link': result[i]['link']}) == 0:
            count_new += 1
            vacancies.insert_one(result[i])
    print(f'Добавлено {count_new} новых вакансий, обновлено {count_upd} старых вакансий')
    return vacancies


def add_to_db(vacancies):
    result = search_vacancies()
    vacancies.delete_many({})  # т. к. функция, пропускающая дубли, по заданию идёт отдельно, то удаляем всю старую
    # базу при запуске данной функции
    vacancies.insert_many(result)
    return vacancies


def find_salary(vacancies):
    salary = float(input('Введите желаемую сумму: '))
    filtered_list = []
    for vacancy in vacancies.find({"$or": [{'min_salary': {'$gt': salary}}, {'min_salary': {'$gt': salary}}]}):
        pprint(vacancy)
        filtered_list.append(vacancy)
    print(f'Найдено {len(filtered_list)} вакансий')
    return filtered_list


# add_to_db(vacancies)
# find_salary(vacancies)
# no_doubles(vacancies)

# print(vacancies.estimated_document_count())
