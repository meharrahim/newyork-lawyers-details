# -*- coding: utf-8 -*-
import scrapy

class AvvoSpider(scrapy.Spider):
    name = 'avvo'
    allowed_domains = ['www.avvo.com/all-lawyers/ny/new_york.html']
    start_urls = ['http://www.avvo.com/all-lawyers/ny/new_york.html',
    'https://www.avvo.com/find-a-lawyer/all-practice-areas/ny/new_york']


    # allowed_domains = ['www.youtube.com']
    # start_urls = ['https://www.youtube.com/']




    def parse(self, response):

        #Get the links of all practice areas of lawyers
        area_titles = response.xpath('//*[@id="areas-of-law"]/div[*]/div[*]/*/a/@href | //*[@id="areas-of-law"]/div[*]/div[*]/*/*/a/href').extract()
        print("\n \n \n practice areas" , area_titles)
        