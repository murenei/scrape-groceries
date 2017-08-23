import scrapy


class AldiSpider(scrapy.Spider):
    name = "aldi"

    def start_requests(self):
        urls = [
        'https://www.aldi.com.au/en/groceries/home-of-the-lowest-prices/',  # THIS IS THE MAIN PRODUCT LISTING PAGE
        # 'https://www.aldi.com.au/en/groceries/awards/',       # SKIP: NO PRICES
        'https://www.aldi.com.au/en/groceries/baby-care/',
        'https://www.aldi.com.au/en/groceries/chocolate/',
        'https://www.aldi.com.au/en/groceries/coffee/',
        # 'https://www.aldi.com.au/en/groceries/gluten-free/',      # SKIP: NO PRICES
        'https://www.aldi.com.au/en/groceries/laundry/',
        'https://www.aldi.com.au/en/groceries/liquor/',     # THIS IS THE ONLY CATEGORY WITH SUB-CATEGORIES
        'https://www.aldi.com.au/en/groceries/olive-oils/',
        'https://www.aldi.com.au/en/groceries/skin-care/',
        # 'https://www.aldi.com.au/en/groceries/testers-club-product-reviews/', # IGNORE: CONTAINS PRODUCT REVIEWS ONLY
        # 'https://www.aldi.com.au/en/groceries/recipes/',      # IGNORE FOR NOW: CONTAINS RECIPES ONLY
        # 'https://www.aldi.com.au/en/groceries/hells-kitchen/'   # IGNORE: RECIPES FROM HELL'S KITCHEN
    ]
        for url in urls:
            if url.split('/')[-2]!='liquor':
                yield scrapy.Request(url=url, callback=self.parse_details)
            else:
                yield scrapy.Request(url=url, callback=self.parse_categories)


    def parse_categories(self, response):
        urls = response.css('div.csc-textpic-imagecolumn > a::attr(href)').extract()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_details)


    def parse_details(self, response):
        listings = response.css('div.box')
        for product in listings:
            yield {
                'page': response.url.split('/')[-2],
                'product_name': (product.css('h2.box--description--header > a::text').extract_first() or '').strip(),
                'product_amount': (product.css('div.box--price > span.box--amount::text').extract_first() or ''),
                'product_price': (product.css('span.box--value::text').extract_first() or '') + (product.css('span.box--decimal::text').extract_first() or ''),
                'base_price': (product.css('div.box--price > span.box--baseprice::text').extract_first() or ''),
                'product_link': (product.css('a.box--description--header--link::attr(href)').extract_first() or ''),
                'former_price': (product.css('div.box--price > span.box--former-price::text').extract_first() or '').strip(),
                'image_link': (product.css('a.box--image--link > img::attr(src)').extract_first() or ''),
                'product_description': '',
            }