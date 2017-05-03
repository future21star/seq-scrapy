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

class Fitness19Spider(scrapy.Spider):
		name = "fitness19"
		uid_list = []
		start_urls = ['http://www.fitness19.com/convenient-locations/']
		def parse(self, response):
			try:
				for state in response.xpath('//section[@id="location-list"]//a'):
					yield scrapy.Request(url=state.xpath('./@href').extract_first(), callback=self.parse_url)
			except:
				pass
		def parse_url(self, response):
			try:
				for state in response.xpath('//section[@id="locations_list"]//a'):
					yield scrapy.Request(url=state.xpath('./@href').extract_first(), callback=self.parse_store)
			except:
				pass
		def parse_store(self, response):
			try:
				store = response.xpath('//div[@class="location-sidebar"]')[0]
				item = ChainItem()
				item['store_number'] = ""
				item['store_name'] = ""
				item['address'] = self.validate(response.xpath('.//section[@id="location-address"]/p/text()'))
				item['address2'] = self.validate(store.xpath('./address2/text()'))
				item['city'] = response.xpath('.//section[@id="location-address"]/p/text()').extract()[1].split(',')[0].strip()
				item['state'] = response.xpath('.//section[@id="location-address"]/p/text()').extract()[1].split(',')[1].strip().split()[0].strip()
				item['zip_code'] = response.xpath('.//section[@id="location-address"]/p/text()').extract()[1].split(',')[1].strip().split()[1].strip()
				item['country'] = "United States" 
				item['phone_number'] = response.xpath('.//section[@id="location-address"]/p/text()').extract()[2]
				item['store_hours'] = ""
				hours = response.xpath('.//section[@id="location-hours"]/dl//text()').extract()
				for hour in hours: 
					if hours.index(hour) % 2 == 0:
						item['store_hours'] += hour + ":";
					else:
						item['store_hours'] += hour + ";"
				pos = response.body.find('LatLng') + 7
				item['latitude'] = ""
				item['longitude'] = ""
				while response.body[pos] != ',':
					item['latitude'] += response.body[pos]
					pos += 1
				item['latitude'] = item['latitude'].strip()
				pos += 1
				while response.body[pos] != ')':
					item['longitude'] += response.body[pos]
					pos += 1
				item['longitude'] = item['longitude'].strip()
				#item['store_type'] = info_json["@type"]
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