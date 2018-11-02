# -*- coding: utf-8 -*-
import scrapy


class AvvoSpider(scrapy.Spider):
    name = 'avvo'
    allowed_domains = ['https://www.avvo.com/all-lawyers/ny.html']
    start_urls = ['http://https://www.avvo.com/all-lawyers/ny.html/']

    def parse(self, response):
        pass
