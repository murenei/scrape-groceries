# -*- coding: utf-8 -*-
import scrapy


class AldiSpider(scrapy.Spider):
    name = 'aldi'
    allowed_domains = ['aldi.com.au']
    start_urls = ['http://aldi.com.au/']

    def parse(self, response):
        pass
