import unittest
from app.crawl import crawl_site


class CrawlTester(unittest.TestCase):
    def test_crawler(self):
        crawl_site('https://yandex.ru', -1)
