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

class NationalsportsSpider(scrapy.Spider):
		name = "nationalsports"
		uid_list = []
		start_urls = ['http://www.nationalsports.com/store-locator.asp']

		def parse(self, response):
			try:
				for store in response.xpath('//a[@class="newsList"]/@href').extract():
					url = "http://www.nationalsports.com" + store
					item = ChainItem()
					item['store_number'] = store.split('id=')[-1]
					request = scrapy.Request(url=url, callback=self.parse_store)
					request.meta['item'] = item
					if url not in self.uid_list:
						self.uid_list.append(url)
					print "-------------------------------------------------"
					print len(self.uid_list)
					print "-------------------------------------------------"
					yield request
			except:
				pdb.set_trace()
				pass

		def parse_store(self, response):
			try:
				store = response
				item = response.meta['item']
				item['store_name'] = self.validate(store.xpath('//div[@class="storeTitle"]/text()'))
				addr = store.xpath('//div[@style="float:left; width:450px;"]/p[1]/text()').extract()
				item['address'] = addr[0].strip()
				item['address2'] = ""
				item['city'] = addr[1].split(',')[0].strip()
				item['state'] = addr[1].split(',')[1].strip()
				item['zip_code'] = addr[2].strip()
				item['country'] = "Canada" 
				item['phone_number'] = store.xpath('//div[@style="float:left; width:450px;"]/p[2]/text()').extract()[1].strip()
				hours = store.xpath('//div[@style="float:left; width:450px;"]/p[3]/text()').extract()
				hours = [a.strip() for a in hours if a.strip() != ""]
				item['store_hours'] = ";".join(hours)
				try:
					lat_lng = self.validate(store.xpath('//a[contains(@href, "http://maps.google.com/maps")]/@href'))
					item['latitude'] = lat_lng.split("sll=")[-1].split(',')[0]
					item['longitude'] = lat_lng.split("sll=")[-1].split(',')[1].split('&')[0]
				except:
					try:
						lat_lng = self.validate(store.xpath('//a[contains(@href, "https://www.google.com/maps")]/@href'))
						item['latitude'] = lat_lng.split("@")[-1].split(',')[0]
						item['longitude'] = lat_lng.split("@")[-1].split(',')[1].split(',')[0]					
					except:
						item['latitude'] = ""
						item['longitude'] = ""
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




