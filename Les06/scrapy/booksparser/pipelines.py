# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class BooksparserPipeline:
    def __init__(self):  # Конструктор, где инициализируем подключение к СУБД
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.books_scrapy

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]  # Выбираем коллекцию по имени паука
        collection.insert_one(item)  # Добавляем в базу данных
        return item
