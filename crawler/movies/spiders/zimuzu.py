# -*- coding: utf-8 -*-
import scrapy


class ZimuzuSpider(scrapy.Spider):
    name = "zimuzu"
    allowed_domains = ["zimuzu.tv"]
    start_urls = (
        'http://www.zimuzu.tv/eresourcelist?page=1&channel=&area=&category=&format=&year=&sort=',
    )

    def parse(self, response):
        pass
