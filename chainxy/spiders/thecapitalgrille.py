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

class ThecapitalgrilleSpider(scrapy.Spider):
		name = "thecapitalgrille"
		uid_list = []
		start_urls = ['http://www.thecapitalgrille.com/locations/all-locations']
		count = 0
		domain = "http://www.thecapitalgrille.com"

		def parse(self, response):
			try:
				for url in response.xpath('//input[@id="redirectLocationUrl"]/@value').extract():
					item = ChainItem()
					item['store_number'] = url.split('/')[-1]
					request = scrapy.Request(url=self.domain+url, callback=self.parse_store)
					request.meta['item'] = item
					yield request
	 		except:
	 			pass

		def parse_store(self, response):
			try:
				item = response.meta['item']
				item['store_name'] = ""
				address = self.validate(response.xpath('//input[@id="restAddress"]/@value')).split(',')
				item['address'] = ','.join(address[:-3]).strip()
				item['address2'] = ""
				item['city'] = address[-3].strip()
				item['state'] = address[-2].strip()
				item['zip_code'] = address[-1].strip()
				item['country'] = "United States" 
				item['phone_number'] = response.xpath('//div[@class="left-bar"][1]/p[1]/text()').extract()[-1].strip()
				hours = response.xpath('//span[@id="popRestHrs"]//text()').extract()
				item['store_hours'] = ""
				lat_lng = self.validate(response.xpath('//input[@id="restLatLong"]/@value')).split(',')
				item['latitude'] = lat_lng[0].strip()
				item['longitude'] = lat_lng[1].strip()
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