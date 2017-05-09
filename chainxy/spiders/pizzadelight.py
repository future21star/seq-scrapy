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

class PizzadelightSpider(scrapy.Spider):
		name = "pizzadelight"
		uid_list = []
		start_urls = ['https://www.pizzadelight.com/en/find-a-restaurant.html']
		count = 0
		domain = "https://www.pizzadelight.com/"

		def parse(self, response):
			try:
				for url in response.xpath('//table[1]//a[contains(@href,"en/find-a-restaurant/pizzeria/")]/@href').extract():
					item = ChainItem()
					item['store_number'] = url.split('/')[-1].split('-')[0]
					request = scrapy.Request(url=self.domain+url, callback=self.parse_store)
					request.meta['item'] = item
					yield request 
					# yield scrapy.Request(url="http://www.johnnybruscos.com/location/hickory-flat/", callback=self.parse_store)
	 		except:
	 			pass

		def parse_store(self, response):
			store = response.xpath('//div[@class="colPrincipal"]')
			try:
				item = response.meta['item']
				item['store_name'] = ""
				info = store.xpath('./p[@class="interstate"]/text()').extract()
				item['address'] = info[2].strip()
				item['address2'] = ""
				item['city'] = info[3].strip().replace('\r', '').replace('\n','').replace('\t','').split('(')[0].strip()
				item['state'] = info[3].strip().replace('\r', '').replace('\n','').replace('\t','').split('(')[1].strip()[:-1]
				item['zip_code'] = info[4].strip()
				item['country'] = "Canada" 
				item['phone_number'] = info[1].strip()
				item['store_hours'] = ";".join(response.xpath('//div[@class="colPrincipal"]/div[@class="interstate"][1]/p/text()').extract())
				pos = response.body.find('LatLng(') + 7
				item['latitude'] = ""
				while response.body[pos] != ",":
					item['latitude'] += response.body[pos]
					pos += 1
				item['latitude'] = item['latitude'].strip()
				pos += 1
				item['longitude'] = ""
				while response.body[pos] != ")":
					item['longitude'] += response.body[pos]
					pos += 1
				item['longitude'] = item['longitude'].strip()
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = 0
				yield item
			except:
				pdb.set_trace()
				pass			

		def validate(self, xpath):
			try:
				return xpath.extract_first().strip()
			except:
				return ""

		def getInfo(self, response):
			try:
				start = response.body.find("location_data.push( ") + 20
				pos = response.body.find("location_data.push( ") + 20
				info = ""
				while response.body[pos] != '}':
					if response.body[pos:pos+2] != "\'":
						info += response.body[pos]
					else:
						info += "'"
					pos += 1
				info += '}'
				return info.decode('utf8').replace("\'", "").replace('\t','').replace('\n','')
			except:
				return ""

		def getValue(self, info, property):
			try:
				pos = info.find(property + ":") + len(property) + 2
				value = ""
				while info[pos] != ",":
					value += info[pos]
					pos += 1
				return value
			except:
				return ""

		def getSpecificValue(self, info, property):
			try:
				pos = info.find(property) + len(property) + 3
				value = ""
				while info[pos:pos+2] != "</":
					value += info[pos]
					pos += 1
				return value.strip()
			except:
				return ""