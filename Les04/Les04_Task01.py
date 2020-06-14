# 1)Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex.news
# Для парсинга использовать xpath. Структура данных должна содержать:
# название источника,
# наименование новости,
# ссылку на новость,
# дата публикации
# 2)Сложить все новости в БД

import datetime
import time
from pymongo import MongoClient
from pprint import pprint
import requests
from lxml import html


def news_yandex(news_list, headers):
    main_link = 'https://yandex.ru/'
    response = requests.get('https://yandex.ru/news/', headers=headers)
    dom = html.fromstring(response.text)
    news_blocks = dom.xpath("//td[@class='stories-set__item'] | //div[@class='stories-set__main-item']")
    for news in news_blocks:
        news_summary = {}
        rel_link = news.xpath(".//a[contains(@class, 'link_theme_black')]/@href")
        news_link = main_link + rel_link[0]
        news_title = news.xpath(".//a[contains(@class, 'link_theme_black')]/text()")
        news_source_date = news.xpath(".//div[contains(@class, 'story__date')]/text()")[0]
        news_date = f'{datetime.date.today()} {news_source_date[len(news_source_date) - 6:]}'
        news_source = f'{news_source_date[:-6]}'
        news_summary['link'] = news_link
        news_summary['title'] = news_title
        news_summary['source'] = news_source
        news_summary['date'] = news_date
        news_list.append(news_summary)
    return news_list


def news_mail(news_list, headers):
    main_link = 'https://news.mail.ru'
    response = requests.get(main_link, headers=headers)
    dom = html.fromstring(response.text)
    news_blocks = dom.xpath("//a[contains(@class, 'newsitem__title')] | //li[contains(@class, 'list__item')] | "
                            "//div[contains(@class, 'daynews__item')]")
    for news in news_blocks:
        news_summary = {}
        news_title = news.xpath(".//text()")[0]
        news_title = news_title.replace('\xa0', ' ')
        rel_link = news.xpath(".//@href")
        if rel_link[0][0] == 'h':
            news_link = rel_link[0]
        else:
            news_link = main_link + rel_link[0]
        response_source = requests.get(news_link, headers=headers)
        dom_source = html.fromstring(response_source.text)
        news_source = dom_source.xpath("//div[contains(@class, 'breadcrumbs')]"
                                       "//span[contains(@class, 'link__text')]//text()")[0]
        news_source_date = dom_source.xpath("//div[contains(@class, 'breadcrumbs')]"
                                            "//span[contains(@class, 'note__text')]/@datetime")[0]
        news_day = news_source_date[:10]
        news_time = news_source_date[11:19]
        news_date = f'{news_day} {news_time}'
        news_summary['title'] = news_title
        news_summary['link'] = news_link
        news_summary['source'] = news_source
        news_summary['date'] = news_date
        news_list.append(news_summary)
        time.sleep(2)  # насколько я понял, меня мэйл иногда начинал банить из-за большого количества запросов,
        # т. к. часть ответов была под конец пустой
    return news_list


def news_lenta(news_list, headers):
    main_link = 'https://lenta.ru'
    response = requests.get(main_link, headers=headers)
    dom = html.fromstring(response.text)
    news_blocks = dom.xpath("//div[@class='titles']")
    for news in news_blocks:
        news_summary = {}
        news_title = news.xpath(".//text()")[0]
        news_title = news_title.replace('\xa0', ' ')
        rel_link = news.xpath(".//@href")
        news_link = main_link + rel_link[0]
        news_time = news.xpath("..//span[contains(@class, 'time')]/text()")[0]
        news_day = news.xpath("..//span[contains(@class, 'item__date')]/text()")[0]
        news_date = news_day + ' ' + news_time
        news_summary['title'] = news_title
        news_summary['link'] = news_link
        news_summary['source'] = 'LENTA.RU'
        news_summary['date'] = news_date
        news_list.append(news_summary)
    return news_list


news_list = []
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0'}


news_yandex(news_list, headers)
news_lenta(news_list, headers)
news_mail(news_list, headers)
pprint(news_list)
print(f'Добавлено {len(news_list)} новостей')

client = MongoClient('localhost', 27017)
db = client['news']
news = db.news

# news.delete_many({})
news.insert_many(news_list)

print('done')
