# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse  # Для подсказок объекта response
from Les06.scrapy.booksparser.items import BooksparserItem  # Подключаем класс из items


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    # start_urls = ['http://book24.ru/']
    start_urls = ['https://book24.ru/search/?q=%D0%BF%D1%83%D1%82%D0%B5%D1%88%D0%B5%D1%81%D1%82%D0%B2%D0%B8%D1%8F']

    def parse(self, response):
        next_page = response.css('a.catalog-pagination__item:contains("Далее")::attr(href)').extract_first()
        books_links = response.css('div.book__title a.book__title-link::attr(href)').extract()
        for book in books_links:  # Перебираем ссылки
            # Переходим по каждой ссылке и обрабатываем ответ методом book_parse
            yield response.follow(book, callback=self.book_parse)
        # Переходим по ссылке на следующую страницу и возвращаемся к началу метода parse
        yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        book_title = response.css('h1.item-detail__title::text').extract_first()
        book_rate = response.css('span.rating__rate-value::text').extract_first()
        if book_rate is not None:
            book_rate = book_rate.replace(',', '.')
            book_rate = float(book_rate)
        book_url = response.url
        book_author = response.css('a.item-tab__chars-link::text').extract_first()
        book_price = response.css('div.item-actions__price-old::text').extract_first()
        if book_price is not None:
            book_price_sale = response.css('div.item-actions__price b::text').extract_first()
            book_price = book_price[:-3]
        else:
            book_price = response.css('div.item-actions__price b::text').extract_first()
            book_price_sale = None
        book_price = book_price.replace(' ', '')
        book_price = float(book_price)
        if book_price_sale is not None:
            book_price_sale = book_price_sale.replace(' ', '')
            book_price_sale = float(book_price_sale)

        yield BooksparserItem(title=book_title, price=book_price, author=book_author, sale=book_price_sale,
                              rate=book_rate, url=book_url)
