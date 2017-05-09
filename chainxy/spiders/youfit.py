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

class YoufitSpider(scrapy.Spider):
		name = "youfit"
		uid_list = []
		start_urls = ['https://www.youfit.com/find-club/all']
		count = 0
		domain = "https://www.youfit.com"

		def parse(self, response):
			try:
				for store_url in response.xpath("//div[@class='state-locations']/a/@href").extract():
					url = self.domain + store_url
					request = scrapy.Request(url=url, callback=self.parse_store_url)
					yield request
			except:
				pass
		def parse_store_url(self, response):
			try:
				stores = response.xpath('//div[@class="location-address"]')
				for store in stores:
					item = ChainItem()
					item['store_number'] = self.validate(store.xpath('./a[1]/@href')).split('/')[-1].split('-')[-1]
					item['store_name'] = "-".join(self.validate(store.xpath('./a[1]/@href')).split('/')[-1].split('-')[:-1])
					if (len(store.xpath('./a[1]/i')) > 0):
						item['coming_soon'] = 1
					else:
						item['coming_soon'] = 0
					url = self.domain + self.validate(store.xpath('./a[1]/@href'))
					request = scrapy.Request(url=url, callback=self.parse_store)
					request.meta['item'] = item
					yield request
			except:
				pass

		def parse_store(self, response):
			try:
				item = response.meta['item']
				item['address'] = self.validate(response.xpath('//span[@itemprop="streetAddress"]/text()'))
				item['address2'] = ""
				item['city'] = self.validate(response.xpath('//span[@itemprop="addressLocality"]/text()'))
				item['state'] = self.validate(response.xpath('//span[@itemprop="addressRegion"]/text()'))
				item['zip_code'] = self.validate(response.xpath('//span[@itemprop="postalCode"]/text()'))
				item['country'] = "United States" 
				item['phone_number'] = self.validate(response.xpath('//span[@itemprop="telephone"]/text()'))
				hours = response.xpath('//div[@class="club-hours"]/ul/li')
				item['store_hours'] = ""
				for hour in hours:
					item['store_hours'] += self.validate(hour.xpath('./text()[1]')) + ":" + self.validate(hour.xpath('./span/text()')) + ";"
				pos = response.body.find("LatLng(") + 7
				item['latitude'] = ""
				while response.body[pos] != ',':
					item['latitude'] += response.body[pos]
					pos += 1
				item['latitude'] = item['latitude'].strip()
				pos += 1
				item['longitude'] = ""
				while response.body[pos] != ')':
					item['longitude'] += response.body[pos]
					pos += 1
				item['longitude'] = item['longitude'].strip()
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
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