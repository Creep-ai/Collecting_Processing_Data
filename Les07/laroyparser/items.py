# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy.loader.processors import Compose, TakeFirst
import scrapy


def float_price(value):
    value[0] = value[0].replace(' ', '')
    return float(value[0])


def correct_features(features):
    for feature_dict in features:
        for key in feature_dict.keys():
            feature_dict[key] = feature_dict[key].strip()
    return features


def create_folder_id(url):
    url[0] = url[0][url[0].rfind("-") + 1 - len(url[0]):-1]
    return url


class LaroyparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    price = scrapy.Field(input_processor=Compose(float_price), output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    features = scrapy.Field(input_processor=Compose(correct_features))
    folder_id = scrapy.Field(input_processor=Compose(create_folder_id), output_processor=TakeFirst())
