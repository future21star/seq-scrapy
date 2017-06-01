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

class BrookFurniturerentalSpider(scrapy.Spider):
		name = "brookfurniturerental"
		uid_list = []
		start_urls = ['https://www.bfr.com/furniture-rental/showroom-locations/']
		count = 0
		domain = "https://www.bfr.com"

		def parse(self, response):
			try:
				for city in response.xpath('/html/body/main/div[2]/div[4]/div[1]//a[contains(@href, "/furniture-rental/showroom-locations/")]/@href').extract():
					url = self.domain + city
					yield scrapy.Request(url=url, callback=self.parse_store)
			except:
				pass 

		def parse_store(self, response):
			try:
				item = ChainItem()
				item['store_number'] = ""
				item['store_name'] = response.xpath('//h1[contains(@style,"text-align: center;")]/text()').extract_first().strip()
				addr = response.xpath('//div[@class="img-repsonsive"]')[0].xpath('./div[2]/text()').extract()
				addr = [a.strip() for a in addr if a.strip() != ""]
				item['address'] = " ".join(addr[:-1]).strip()
				item['address2'] = ""
				if not "& Surrounding Areas" in addr[-1]:
					item['city'] = addr[-1].split(',')[0].strip()
					item['state'] = addr[-1].split(',')[-1].split()[0].strip()
					item['zip_code'] = addr[-1].split(',')[-1].split()[1].strip()
				else:
					try:
						item['city'] = addr[0].split(',')[0].split()[-1].strip()
						item['state'] = addr[0].split(',')[-1].strip()
						item['zip_code'] = ""
					except:
						item['city'] = addr[0].split('/')[0].split()[-1].strip()
						item['state'] = addr[1].split('&')[0].strip()
						item['zip_code'] = ""
				item['country'] = "United States" 
				item['phone_number'] = response.xpath('//span[@style="font-family: minion-pro;"]')[1].xpath('./text()').extract_first().strip()
				item['store_hours'] = response.xpath('//span[@style="font-family: minion-pro;"]')[2].xpath('./text()').extract_first().strip()
				item['latitude'] = response.body.split('3d')[1].split('!')[0]
				item['longitude'] = response.body.split('2d')[1].split('!')[0]
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

		def isNumber(self, number):
			count = 0
			for char in number:
				if char.isdigit():
					count += 1
			return count > 5

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