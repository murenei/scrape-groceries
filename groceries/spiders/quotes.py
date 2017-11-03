# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    login_url = 'http://quotes.toscrape.com/login'
    start_urls = [login_url]



    def parse_item(self, response):
        token = response.css('input[name="csrf_token"]::attr(value)').extract_first()

        data = {
            'csrf_token': token,
            'username': 'abc',
            'password': 'abc'
        }

        yield scrapy.FormRequest(url=self.login_url, formdata=data, callback=self.parse_tags)

    def parse_tags(self, response):
        # collect the goodreads tags
        for quote in response.css('div.quotes').extract():
            yield {
                'author': quote.css('small.author::text').extract_first()
            }