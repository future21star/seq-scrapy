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

class ModpizzaSpider(scrapy.Spider):
		name = "modpizza"
		uid_list = []
		domain = "https://www.metro.ca"
		start_urls = ['https://modpizza.com/store-directory/']

		def parse(self, response):
			for url in response.xpath('//div[contains(@class, "all-caps")]/a/@href').extract():
				request = scrapy.Request(url=url, callback=self.parseStore)
				yield request

		def parseStore(self, response):
			try:
				item = ChainItem()
				base = len(response.xpath('//div[@class="cs m-t-1 m-b-1"]'))
				item['store_number'] = ""
				item['store_name'] = self.validate(response.xpath('//div[contains(@class, "bh-sl-store-info")]/h3/text()')).split('\xe2\x80\x93')[0].strip()
				item['address'] = self.validate(response.xpath('//div[contains(@class, "bh-sl-store-info")]/div[%s]/text()' % str(base + 1)))
				item['address2'] = ""
				item['city'] = self.validate(response.xpath('//div[contains(@class, "bh-sl-store-info")]/div[%s]/text()' % str(base + 3))).split(',')[0]
				item['state'] = self.validate(response.xpath('//div[contains(@class, "bh-sl-store-info")]/div[%s]/text()' % str(base + 3))).split(',')[1].strip().split()[0]
				item['zip_code'] = self.validate(response.xpath('//div[contains(@class, "bh-sl-store-info")]/div[%s]/text()' % str(base + 3))).split(',')[1].strip().split()[1]
				item['country'] = "United States" 
				try:
					item['phone_number'] = self.validate(response.xpath('//a[@class="hidden-md-up"]/text()'))
				except:
					item['phone_number'] = ""
				item['latitude'] = response.xpath('//div[contains(@class, "bh-sl-map--singl")]/@data-lat').extract_first()
				item['longitude'] = response.xpath('//div[contains(@class, "bh-sl-map--singl")]/@data-lng').extract_first()
				try:
					item['store_hours'] = response.xpath('//div[contains(@class, "bh-sl-store-info")]/div[5]/text()').extract_first().replace(' ', ':') + ";" + response.xpath('//div[contains(@class, "bh-sl-store-info")]/div[5]/text()').extract_first().replace(' ', ':') + ";"
				except:
					item['store_hours'] = ""
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				if len(response.xpath('//span[@class="cs__soon"]')) > 0:
					item['coming_soon'] = 1
				else:
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