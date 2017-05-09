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

class ShiekhshoesSpider(scrapy.Spider):
		name = "shiekhshoes"
		uid_list = []
		start_urls = ['http://www.shiekhshoes.com/stores.aspx']
		count = 0
		domain = "http://www.shiekhshoes.com"

		def parse(self, response):
			for store_url in response.xpath("//table[@class='table table-hover']//td[@class='hidden-xs']/a/@href").extract():
				url = self.domain + store_url
				item = ChainItem()
				item['store_number'] = store_url.split('-')[-1].split('.')[0]
				request = scrapy.Request(url=url, callback=self.parse_store)
				request.meta['item'] = item
				yield request

		def parse_store(self, response):
			try:
				store = response.xpath('//dl[@class="dl-horizontal"]')
				item = response.meta['item']
				item['store_name'] = self.validate(store.xpath('./dd[1]/text()'))
				item['address'] = self.validate(store.xpath('./dd[2]/text()'))
				item['address2'] = ""
				temp = self.validate(store.xpath('./dd[3]/text()'))
				item['city'] = temp.split(',')[0].strip()
				item['state'] = temp.split(',')[1].split()[0].strip()
				item['zip_code'] = temp.split(',')[1].split()[1].strip()
				item['country'] = "United States" 
				item['phone_number'] = self.validate(store.xpath('./dd[4]/a/text()'))
				if self.validate(store.xpath('./dt[6]/text()')) == 'Monday':
					item['store_hours'] = self.validate(store.xpath('./dt[6]/text()')) + ":" + self.validate(store.xpath('./dd[7]/text()')) + ";" + self.validate(store.xpath('./dt[7]/text()')) + ":" + self.validate(store.xpath('./dd[8]/text()')) + ";" + self.validate(store.xpath('./dt[8]/text()')) + ":" + self.validate(store.xpath('./dd[9]/text()')) + ";" + self.validate(store.xpath('./dt[9]/text()')) + ":" + self.validate(store.xpath('./dd[10]/text()')) + ";" + self.validate(store.xpath('./dt[10]/text()')) + ":" + self.validate(store.xpath('./dd[11]/text()')) + ";" + self.validate(store.xpath('./dt[11]/text()')) + ":" + self.validate(store.xpath('./dd[12]/text()')) + ";" + self.validate(store.xpath('./dt[12]/text()')) + ":" + self.validate(store.xpath('./dd[13]/text()')) + ";"
				else:
					item['store_hours'] = ''
				item['latitude'] = self.validate(response.xpath('//input[@id="coordinates"]/@value')).split(',')[0].strip()
				item['longitude'] = self.validate(response.xpath('//input[@id="coordinates"]/@value')).split(',')[1].strip()
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