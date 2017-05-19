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

class ArcthriftSpider(scrapy.Spider):
		name = "arcthrift"
		uid_list = []
		start_urls = ['https://www.arcthrift.com/location/store-locations.html']

		def parse(self, response):
			for store in response.xpath("//div[@class='com_locator_entry']/div"):					
				item = ChainItem()
				item['store_number'] = ""
				item['store_name'] = self.validate(store.xpath('./h2/a/text()'))
				addr = self.validate(store.xpath('.//span[@class="line_item address2"]/text()'))
				item['address'] = addr.split(',')[0]
				item['address2'] = ""
				# if item['address'] in ["2780 South Academy Blvd."]:
				# 	pdb.set_trace()
				if addr.split(',')[-1].strip().count(' ') > 1:
					item['city'] = " ".join(addr.split(',')[-1].split()[:-2])
					item['state'] = addr.split(',')[-1].split()[-2]
					item['zip_code'] = addr.split(',')[-1].split()[-1]
				else:
					item['city'] = addr.split(',')[0].split()[-1]
					item['state'] = addr.split(',')[-1].split()[0]
					item['zip_code'] = " ".join(addr.split(',')[-1].split()[1:])					
				item['country'] = "United States" 
				item['phone_number'] = self.validate(store.xpath('.//span[@class="line_item phone"]/text()'))
				hours = response.xpath('//div[@class="custom"][2]/ul[1]//text()').extract()
				hours = [a.strip() for a in hours if a.strip() != ""]
				item['store_hours'] = ";".join(hours)
				try:
					lat_lng = self.validate(store.xpath('./h2/a/@href'))
					item['latitude'] = lat_lng.split('@')[1].split(',')[0]
					item['longitude'] = lat_lng.split('@')[1].split(',')[1].split(',')[0]
				except:
					item['latitude'] = ""
					item['longitude'] = ""
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = 0
				yield item		

		def parse_hour(self, response):
			try:
				store = yaml.load(response.body.split("var locationList = '")[-1].split('},]}')[0] + '},]}')['locationData'][0]
				item = response.meta['item']
				item['store_hours'] = store['LobbyHour']
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




