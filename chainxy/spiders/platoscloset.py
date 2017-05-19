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

class platosclosetSpider(scrapy.Spider):
		name = "platoscloset"
		uid_list = []
		start_urls = ['http://www.platoscloset.com/locations']

		def parse(self, response):
			for state in response.xpath("//svg[@id='us-map']/a").extract():
				url = "http://www.platoscloset.com" + state.split('xlink:href="')[-1].split('"')[0]
				yield scrapy.Request(url=url, callback=self.parse_state)

		def parse_state(self, response):
			for store in response.xpath('//div[@class="location-info-card bg-purple"]'):
				item = ChainItem()
				item['store_number'] = self.validate(store.xpath('./div[@class="location-links"]/a/@data-storenum'))
				url = "http://www.platoscloset.com/" + self.validate(store.xpath('./div[@class="location-name"]/text()'))
				request = scrapy.Request(url=url, callback=self.parse_store)
				request.meta['item'] = item
				yield request

		def parse_store(self, response):
			store = response
			item = response.meta['item']
			item['store_name'] = ""
			item['address'] = self.validate(store.xpath('//div[@class="address-line"][1]/text()'))
			item['address2'] = ""
			addr = self.validate(store.xpath('//div[@class="address-line"][3]/text()')).split(',')
			item['city'] = addr[0].strip()
			item['state'] = addr[1].strip()
			item['zip_code'] = addr[2].strip()
			item['country'] = "United States" 
			item['phone_number'] = self.validate(store.xpath('//div[@class="location-phone"][1]/text()'))
			hours = store.xpath('//div[@class="extended-hours bg-magenta"]/table/tr')
			item['store_hours'] = ""
			for hour in hours:
				if hours.index(hour) > 0:
					hour_content = hour.xpath('.//text()').extract()
					hour_content = [a.strip() for a in hour_content if a.strip() != ""]
					item['store_hours'] += hour_content[0] + ":" + hour_content[1] + ";"
			lat_lng = self.validate(store.xpath('//img[contains(@src, "http://maps.googleapis.com")]/@src'))
			if lat_lng != "":
				item['latitude'] = lat_lng.split('markers=')[1].split(',')[0]
				item['longitude'] = lat_lng.split('markers=')[1].split(',')[1].split('&')[0]
			else:
				item['latitude'] = ""
				item['longitude'] = ""
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




