import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb
import unicodedata
import yaml
class KeySpider(scrapy.Spider):
		name = "key"
		uid_list = []
		start_urls = ["https://locations.key.com/index.html"]
			
		def parse(self, response):
			states = response.xpath('//a[@class="c-directory-list-content-item-link"]/@href').extract()
			for state in states:
				url = "https://locations.key.com/" + state
				yield scrapy.Request(url=url, callback=self.parse_state)

		def parse_state(self, response):
			cities = response.xpath('//a[@class="c-directory-list-content-item-link"]/@href').extract()
			for city in cities:
				url = "https://locations.key.com/" + city
				if city.count("/") == 2:
					yield scrapy.Request(url=url, callback=self.parse_store)
				else:
					yield scrapy.Request(url=url, callback=self.parse_city)

		def parse_city(self, response):
			stores = response.xpath('//h2[@class="c-location-grid-item-title"]/a[1]/@href').extract()
			for store in stores:
				url = "https://locations.key.com/" + store.split("../")[-1]
				yield scrapy.Request(url=url, callback=self.parse_store)

		def parse_store(self, response):
			try:
				item = ChainItem()
				item['store_number'] = ""
				item['store_name'] = self.validate(response.xpath('//h1[@id="location-name"]/text()'))
				item['store_type'] = ""
				item['address'] = self.validate(response.xpath('//span[@class="c-address-street-1"]/text()'))
				item['address2'] = self.validate(response.xpath('//span[@class="c-address-street-2"]//text()'))
				item['city'] = self.validate(response.xpath('//span[@itemprop="addressLocality"]//text()'))
				item['state'] = self.validate(response.xpath('//abbr[@itemprop="addressRegion"]//text()'))
				item['zip_code'] = self.validate(response.xpath('//span[@itemprop="postalCode"]//text()'))
				item['country'] = self.validate(response.xpath('//abbr[@itemprop="addressCountry"]//@title'))
				item['phone_number'] = self.validate(response.xpath('//span[@itemprop="telephone"]//text()'))
				item['store_hours'] = ""
				hours = json.loads(self.validate(response.xpath('//div[@class="c-location-hours-details-wrapper js-location-hours"]/@data-days')))
				for hour in hours:
					try:
						item['store_hours'] += hour["day"] + ":" + str(hour["intervals"][0]["start"]).replace("00",":00") + "-" + str(hour["intervals"][0]["end"]).replace("00",":00") + ";"
					except:
						item['store_hours'] += hour["day"] + ": ;"
				item['latitude'] = response.body.split('latitude":')[-1].split(',')[0]
				item['longitude'] = response.body.split('longitude":')[-1].split(',')[0]
				item['other_fields'] = ""
				item['coming_soon'] = 0
				yield item
			except:
				pass			

		def validate(self, xpath):
			try:
				return self.replaceUnknownLetter(xpath.extract_first().strip())
			except:
				return ""

		def replaceUnknownLetter(self, source):
			try:
				formatted_value = source.encode('utf8').replace('\xc3', '').replace('\xa9', 'e').replace('\xa8', 'e').replace('\xb4', 'o').replace('\xb3', 'o').replace('\xb9', 'u').replace('\xba', 'u').replace('\x89', 'E').replace('\xaa', 'e').replace('\x89', 'E').replace('\xa2', 'a').replace('\xac', 'i').replace('\xad', 'i').replace('\xae', 'i')
				# if "x8" in formatted_value or "x9" in formatted_value or "xa" in formatted_value or "xb" in formatted_value:
				# 	pdb.set_trace()
				return formatted_value
			except:
				return source
		def format(self, item):
			try:
				return unicodedata.normalize('NFKD', item).encode('ascii','ignore').strip()
			except:
				return ''			




