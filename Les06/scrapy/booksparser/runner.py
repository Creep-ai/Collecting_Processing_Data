from scrapy.crawler import CrawlerProcess  # Импортируем класс для создания процесса
from scrapy.settings import Settings  # Импортируем класс для настроек

from Les06.scrapy.booksparser import settings  # Наши настройки
from Les06.scrapy.booksparser.spiders.labirint import LabirintSpider  # Класс паука
from Les06.scrapy.booksparser.spiders.book24 import Book24Spider  # Класс второго паука

if __name__ == '__main__':
    crawler_settings = Settings()  # Создаем объект с настройками
    crawler_settings.setmodule(settings)  # Привязываем к нашим настройкам

    process = CrawlerProcess(settings=crawler_settings)  # Создаем объект процесса для работы
    process.crawl(LabirintSpider)
    process.crawl(Book24Spider)

    process.start()  # Пуск
