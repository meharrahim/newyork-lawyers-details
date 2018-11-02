# -*- coding: utf-8 -*-
import scrapy


class AvvoSpider(scrapy.Spider):
    name = 'avvo'
    allowed_domains = ['www.avvo.com/all-lawyers/ny/new_york.html']
    start_urls = ['http://www.avvo.com/all-lawyers/ny/new_york.html']

    def parse(self, response):
        