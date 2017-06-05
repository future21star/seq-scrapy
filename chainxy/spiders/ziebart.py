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
class ZiebartSpider(scrapy.Spider):
		name = "ziebart"
		uid_list = []
		domain = "http://ziebart.com"

		def __init__(self):
			place_file = open('cities_us.json', 'rb')
			self.place_reader = json.load(place_file)

		def start_requests(self):
			for info in self.place_reader:
				city = info['city'].replace(" ", "%20")
				url = "http://ziebart.com/find-my-local-ziebart?lat=%s&lng=%s&search=%s&sel=10000" % (info['latitude'], info['longitude'], info['city'].replace(' ','+'))
				# url = "http://ziebart.com/find-my-local-ziebart?lat=39.5145515&lng=-76.4110732&search=Fallston&sel=100"
				yield scrapy.Request(url=url, callback=self.parse)

		def parse(self, response):
			for store in response.xpath('//a[contains(@href, "/find-my-local-ziebart/location/")]/@href').extract():
				url = self.domain + store
				yield scrapy.Request(url=url, callback=self.parse_store)

		def parse_store(self, response):
			try:
				store = response
				item = ChainItem()
				item['store_number'] = ""
				item['store_name'] = self.validate(store.xpath('//span[@itemprop="name"]/text()'))
				item['address'] = self.validate(store.xpath('//span[@itemprop="streetAddress"]/text()'))
				item['address2'] = ""
				item['city'] = self.validate(store.xpath('//span[@itemprop="addressLocality"]/text()'))
				item['state'] = self.validate(store.xpath('//p[@class="clsAddress"]//span[4]/text()'))
				item['zip_code'] = self.validate(store.xpath('//p[@class="clsAddress"]//span[5]/text()'))
				item['country'] = "United States" 
				item['phone_number'] = self.validate(store.xpath('//span[@itemprop="telephone"]/a/text()'))
				hours = store.xpath('//tbody[@class="clsStoreTiming"]//text()').extract()
				hours = [a.strip() for a in hours if a.strip() != ""]
				days = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
				item['store_hours'] = ""
				for day in days:
					item['store_hours'] += day + ":" + hours[days.index(day)] + ";"
				item['latitude'] = self.validate(store.xpath('//input[@id="hfLatitude"]/@value'))
				item['longitude'] = self.validate(store.xpath('//input[@id="hfLongitude"]/@value'))
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = 0
				yield item
			except:
				pdb.set_trace()
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




