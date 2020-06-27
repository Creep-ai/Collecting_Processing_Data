# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib.parse import urlparse
from pymongo import MongoClient
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class DataBasePipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroymerlin_scrapy

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]  # Выбираем коллекцию по имени паука
        collection.insert_one(item)  # Добавляем в базу данных
        return item


class LaroyparserPipeline:
    def process_item(self, item, spider):
        return item


class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img, meta=item)  # Скачиваем фото и передает item через meta
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        item = request.meta
        # создаём и называем папки согласно id в конце url-адреса
        return f'{item["url"][item["url"].rfind("-") + 1 - len(item["url"]):-1]}/' \
               f'{os.path.basename(urlparse(request.url).path)}'

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
