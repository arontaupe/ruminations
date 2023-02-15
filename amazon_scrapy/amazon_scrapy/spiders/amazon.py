import scrapy
from urllib.parse import urlencode, urljoin
import re
import json
import random
import numpy as np
import pandas as pd

dtd = ['gauzy', 'meshed', 'cracked', 'stratified', 'scaly', 'swirly', 'perforated',
       'pleated', 'flecked', 'fibrous', 'polka-dotted', 'chequered', 'blotchy', 'stained',
       'crystalline', 'porous', 'banded', 'lacelike', 'sprinkled', 'bubbly', 'lined', 'veined',
       'bumpy', 'paisley', 'potholed', 'waffled', 'pitted', 'frilly', 'spiralled', 'knitted', 'grooved',
       'dotted', 'interlaced', 'crosshatched', 'wrinkled', 'smeared', 'striped', 'braided', 'freckled',
       'cobwebbed', 'honeycombed', 'woven', 'matted', 'zigzagged', 'marbled', 'studded', 'grid']

addon = ['fidget toys', 'mothers day gifts', 'air fryer', 'led lights', 'apple watch band', 'candy',
           'tv stand', 'gaming chair', 'iphone case', 'horror movies', 'gua sha', 'coffee maker', 'crocs',
        'disposable face masks', 'flowers',
           'gadget', 'harness', 'inflatable', 'game', 'animal', 'costume']

queries = []
query = ''
for adj in dtd:
	query = adj + ' ' + random.choice(addon)
	queries.append(query)
#print(queries)



class AmazonSpider(scrapy.Spider):
	name = 'amazon'
	allowed_domains = ['amazon.com', 'amazon.de']
	start_urls = ['http://amazon.com/', 'https://amazon.com/']

	#custom_settings = {'CLOSESPIDER_ITEMCOUNT': 8}
	#custom_settings = {'CLOSESPIDER_PAGECOUNT': 1}


	def start_requests(self):
		#queries.to_csv('queries.csv')
		arr = np.asarray(queries)
		pd.DataFrame(arr).to_csv('queries.csv', index=False, header=False)

		for query in queries:
			url = 'https://www.amazon.com/s?' + urlencode({'k': query})
			yield scrapy.Request(url=url, callback=self.parse_keyword_response, meta={"query" : query})

	def parse_keyword_response(self, response):
		products = response.xpath('//*[@data-asin]')

		for product in products:
			asin = product.xpath('@data-asin').extract_first()
			query = response.meta["query"]
			product_url = f"https://www.amazon.com/dp/{asin}"
			yield scrapy.Request(url=product_url, callback=self.parse_product_page, meta={'asin': asin,'query': query})

		next_page = response.xpath('//li[@class="a-last"]/a/@href').extract_first()
		if next_page:
			url = urljoin("https://www.amazon.com", next_page)
			yield scrapy.Request(url=product_url, callback=self.parse_keyword_response)

	def parse_product_page(self, response):
		asin = response.meta['asin']
		query = response.meta["query"]
		title = response.xpath('//*[@id="productTitle"]/text()').extract_first()
		image = None
		try:
			image = re.search('"large":"(.*?)"', response.text).groups()[0]
		except Exception:
			image = None

		rating = response.xpath('//*[@id="acrPopover"]/@title').extract_first()
		number_of_reviews = response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract_first()
		price = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first()

		if not price:
			price = response.xpath('//*[@data-asin-price]/@data-asin-price').extract_first() or \
			        response.xpath('//*[@id="price_inside_buybox"]/text()').extract_first() \
			        or \
					response.xpath('//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
			                            ).extract()
			        #response.css('.a-price span[aria-hidden="true"] ::text').get("")


		bullet_points = response.xpath('//*[@id="feature-bullets"]//li/span/text()').extract()

		yield {'asin'           : asin,
		       'Title'          : title,
		       'MainImage'      : image,
		       'Rating'         : rating,
		       'NumberOfReviews': number_of_reviews,
		       'Price'          : price,
		       'BulletPoints'   : bullet_points,
		       'query'          : query}

	def parse(self, response):
		pass
