# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class InstparserPipeline:
    def process_item(self, item, spider):
        return item


class DataBasePipeline:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.mongo_base = self.client.instagram_scrapy

    def process_item(self, item, spider):
        collection = self.mongo_base['users']
        collection.update_one({'user_id': item['user_id']},
                              {"$set": {'user_id': item['user_id'], 'username': item['username']}}, upsert=True)
        collection = self.mongo_base[item['user_id']]  # Выбираем коллекцию по id пользователя, которого парсим
        # Дропаем ненужные больше поля
        del item['user_id']
        del item['username']
        print(item)
        # Выполняем проверку и вставку документов в БД
        if item['label'] == 'follower':
            collection.replace_one({'follower_id': item['follower_id']}, item, upsert=True)
        elif item['label'] == 'following':
            collection.replace_one({'following_id': item['following_id']}, item, upsert=True)
        return item

    def __del__(self):
        self.client.close()
