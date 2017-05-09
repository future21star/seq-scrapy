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

class RolypolySpider(scrapy.Spider):
		name = "rolypoly"
		uid_list = []
		start_urls = ['http://www.rolypoly.com/locations/loc.php']
		count = 0
		domain = "http://www.rolypoly.com"

		def parse(self, response):
			try:
				for url in response.xpath('//div[@id="leftcontent"]/ul/li/a/@href').extract():
					request = scrapy.Request(url=self.domain+url, callback=self.parse_store)
					yield request
	 		except:
	 			pass

		def parse_store(self, response):
			try:
				stores = response.xpath('//tr[@valign="top"]/td[2]')
				for store in stores:
					item = ChainItem()
					item['store_number'] = ""
					item['store_name'] = ""
					address = store.xpath('./p[1]/text()').extract()
					item['address'] = address[1].strip()
					item['address2'] = ""
					item['city'] = address[-1].split(',')[0].strip()
					item['state'] = address[-1].split(',')[1].split()[0].strip()
					item['zip_code'] = address[-1].split(',')[1].split()[1].strip()
					item['country'] = "United States" 
					item['phone_number'] = self.validate(store.xpath('.//a[contains(@href,"tel:")]/text()'))
					hours = store.xpath('./p[5]/text()').extract()
					hours = filter(lambda a: a.strip()!= "" and a.strip() != "Menu", hours)
					item['store_hours'] = ""
					for hour in hours:
						if (hours.index(hour) % 2 == 0):
							item['store_hours'] += hour.strip() + ":"
						else:
							item['store_hours'] += hour.strip() + ";"
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