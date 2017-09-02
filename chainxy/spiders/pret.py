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

class PretSpider(scrapy.Spider):
		name = "pret"
		uid_list = []
		start_urls = ['http://www.pret.com/en-us/pret-shops']
		count = 0

		def parse(self, response):
			try:
				i = 0
				for store in response.xpath('//div[@class="info"]'):
					pdb.set_trace()
					item = ChainItem()
					url = store.xpath('./h4/a/@href').extract_first()
					if url == None:
						item['address'] = store.xpath('./h4/text()').extract_first()
						item['coming_soon'] = 1
						item['zip_code'] = ""
						item['state'] = ""
						item['city'] = ""
						item['store_name'] = ""
						item['address2'] = ""
						item['country'] = "United States" 
						item['phone_number'] = ""
						item['store_hours'] = ""
						item['latitude'] = ""
						item['longitude'] = ""
						#item['store_type'] = info_json["@type"]
						item['other_fields'] = ""
						yield item
						continue
					address = store.xpath("./p/text()").extract_first().split(',')
					if "60602" in address[-1]:
						item['zip_code'] = "60602"
						item['state'] = "IL"
						item['city'] = "Chicago"
						item['address'] = "108 N State Street"
					elif "60661" in address[-1]:
						item['zip_code'] = "60661"
						item['state'] = "IL"
						item['city'] = "Chicago"
						item['address'] = "500 W Madison St"
					else:
						item['zip_code'] = address[-1].strip()
						item['state'] = address[-2].strip()
						item['city'] = address[-3].strip()
						item['address'] = ",".join(address[:-3]).strip()
					request = scrapy.Request(url=url, callback=self.parse_store, dont_filter=True )
					request.meta['item'] = item
					yield request 
					i += 1
					if i == 1:
						return 
	 		except:
	 			pdb.set_trace()
	 			pass

		def parse_store(self, response):
			try:
				item = response.meta['item']
				# item['store_name'] = ""
				# item['address2'] = ""
				# item['country'] = "United States" 
				# item['phone_number'] = self.validate(response.xpath("//span[@class='number']/text()")).split(':')[-1].strip().replace(' ', '-').strip()
				# hours = response.xpath('//div[contains(@class, "col-holder")]')[6].xpath('.//div[@class="col-sm-6"][2]/div/dl')
				# hours = hours.xpath('.//text()').extract()
				# hours = filter(lambda a: a.strip()!= "", hours)
				# item['store_hours'] = ""
				# for hour in hours:
				# 	if hours.index(hour) % 2 == 0:
				# 		item['store_hours'] += hour + ":"
				# 	else:
				# 		item['store_hours'] += hour + ";"
				# item['store_hours'] = item['store_hours'].strip()						
				# lat_lng = response.xpath('//div[@class="map-canvas"][1]/@data-position').extract_first()
				# item['latitude'] = lat_lng.split(',')[0].strip()
				# item['longitude'] = lat_lng.split(',')[1].strip()
				# #item['store_type'] = info_json["@type"]
				# item['other_fields'] = ""
				# item['coming_soon'] = 0
				yield item
			except:
				pdb.set_trace()
				pass			

		def validate(self, xpath):
			try:
				return xpath.extract_first().strip()
			except:
				return ""
