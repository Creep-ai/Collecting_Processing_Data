# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from Les07.laroyparser.items import LaroyparserItem
from scrapy.loader import ItemLoader


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['http://leroymerlin.ru/']

    def __init__(self, search):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response):
        goods_links = response.css('a.product-name-inner')
        next_page = response.css('a.next-paginator-button')[0]
        print(goods_links)
        for link in goods_links:
            yield response.follow(link, callback=self.parse_goods)
        yield response.follow(next_page, callback=self.parse)

    def parse_goods(self, response: HtmlResponse):
        loader = ItemLoader(item=LaroyparserItem(), response=response)
        loader.add_xpath('photos', '//img[contains(@alt, "product image")]/@src')
        loader.add_xpath('name', '//h1[contains(@class, "header-2")]/text()')
        loader.add_xpath('price', '//uc-pdp-price-view/span[contains(@slot, "price")]/text()')
        loader.add_value('url', response.url)
        loader.add_value('folder_id', response.url)  # Для удобства сопоставления добавляю имя папки
        features = []
        for feature in response.css('dt'):
            feature_dict = {}
            key = feature.css("::text").get()
            value = feature.xpath('./following-sibling::dd/text()').get()
            feature_dict[f'{key}'] = value
            features.append(feature_dict)
        loader.add_value('features', features)
        yield loader.load_item()
