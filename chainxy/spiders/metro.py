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

class MetroSpider(scrapy.Spider):
		name = "metro"
		uid_list = []
		domain = "https://www.metro.ca"
		start_urls = ['https://www.metro.ca/en/find-a-grocery']

		def parse(self, response):
			for url in response.xpath('//a[@class="fs--grocery-detail"]/@href').extract():
				item = ChainItem()
				item['store_number'] = url.split('/')[-1]
				request = scrapy.Request(url=self.domain+url, callback=self.parseStore)
				request.meta['item'] = item
				yield request

		def parseStore(self, response):
			item = response.meta['item']
			item['store_name'] = self.validate(response.xpath('//p[@class="sd--name"]/text()'))
			item['address'] = self.replaceUnknownLetter(' '.join(response.xpath('//div[@class="sd--content"]/p[2]/text()').extract()[0].strip().split()).replace('\n', ' '))
			item['address2'] = ""
			item['phone_number'] = self.replaceUnknownLetter(response.xpath('//div[@class="telephone"]/div[1]/text()[2]').extract_first().strip())
			if len(response.xpath('//div[@class="sd--content"]/p[2]/text()').extract()) > 1:
				info = response.xpath('//div[@class="sd--content"]/p[2]/text()').extract()
			else:
				info = response.xpath('//div[@class="sd--content"]/p[3]/text()').extract()		
			item['city'] = self.replaceUnknownLetter(info[1].strip().split(',')[0].strip())
			item['state'] = self.replaceUnknownLetter(info[1].strip().split(',')[1].strip())
			item['zip_code'] = self.replaceUnknownLetter(info[2].strip())
			item['country'] = "Canada"
			item['latitude'] = self.replaceUnknownLetter(response.xpath('//div[@class="map-canvas"]/@data-store-lat').extract_first())
			item['longitude'] = self.replaceUnknownLetter(response.xpath('//div[@class="map-canvas"]/@data-store-lng').extract_first())
			item['store_hours'] = ""
			days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
			hours = response.xpath('//div[@data-opening="store"]//span[@class="sd-opening-hours"]/text()').extract()
			for hour in hours:
				item['store_hours'] += days[hours.index(hour)] + ":" + hour + ";"
			#item['store_type'] = info_json["@type"]
			item['other_fields'] = ""
			item['coming_soon'] = 0
			yield item

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