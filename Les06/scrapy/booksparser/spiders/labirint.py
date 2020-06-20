# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse  # Для подсказок объекта response
from Les06.scrapy.booksparser.items import BooksparserItem  # Подключаем класс из items


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    # start_urls = ['http://labirint.ru/']
    start_urls = ['https://www.labirint.ru/search/%D0%BF%D1%83%D1%82%D0%B5%D1%88%D0%B5%D1%81%D1%82%D0%B2%D0%B8%D1%8F'
                  '/?stype=0']

    def parse(self, response: HtmlResponse):
        next_page = response.css('div.pagination-next a.pagination-next__text::attr(href)').extract_first()
        books_links = response.css('div.card-column a.cover::attr(href)').extract()
        for book in books_links:  # Перебираем ссылки
            # Переходим по каждой ссылке и обрабатываем ответ методом book_parse
            yield response.follow(book, callback=self.book_parse)
        # Переходим по ссылке на следующую страницу и возвращаемся к началу метода parse
        yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        book_title = response.css('div.prodtitle h1::text').extract_first()
        book_rate = float(response.css('div[id="product-voting-body"] div[id="rate"]::text').extract_first())
        book_author = response.css('div.product-description div.authors a.analytics-click-js::text').extract_first()
        book_url = response.url
        if book_author is None:
            book_author = response.css('div.product-author a span::text').extract_first()
            if book_author is None:
                book_author = 'Автор не найден'
        book_price = response.css('div.buying span.buying-priceold-val-number::text').extract_first()
        if book_price is None:
            book_price = response.css('div.buying span.buying-price-val-number::text').extract_first()
        book_price_sale = response.css('div.buying span.buying-pricenew-val-number::text').extract_first()
        if book_price is not None:
            book_price = float(book_price)
        if book_price_sale is not None:
            book_price_sale = float(book_price_sale)
        yield BooksparserItem(title=book_title, price=book_price, author=book_author,
                              sale=book_price_sale, rate=book_rate, url=book_url)
