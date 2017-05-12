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
from lxml import etree

class RotiSpider(scrapy.Spider):
	name = "roti"
	uid_list = []
	start_urls = ['http://roti.com/locations/']

	def parse(self, response):
		stores = response.xpath('//div[@class="location"]')
		for store in stores:
			item = ChainItem()
			item['store_number'] = ""
			item['store_name'] = self.validate(store.xpath('.//h1/a/text()'))
			addr = store.xpath('./p[1]/text()').extract()
			item['address'] = ""
			item['address2'] = ""
			if len(addr) == 1:
				if 'Coming Soon!' in addr[0]:
					addr[0] = addr[0].replace('- Coming Soon!', '')
				try:
					if len(addr[0].split(',')) in [3, 4]:
						if len(addr[0].split(',')[-1].split()) == 2:
							item['zip_code'] = addr[0].split(',')[-1].split()[-1]
							item['state'] = addr[0].split(',')[-1].split()[0]
							item['city'] = addr[0].split(',')[-2]
							item['address'] = " ".join(addr[0].split(',')[:-2])
						else:
							item['zip_code'] = addr[0].split(',')[-1].split()[-1]
							item['state'] = addr[0].split(',')[-1].split()[-2]
							item['city'] = addr[0].split(',')[-1].split()[-3]
							item['address'] = " ".join(addr[0].split(',')[:-1])
					else:
						if len(addr[0].split(',')[-1].split()) == 3:
							item['zip_code'] = addr[0].split(',')[-1].split()[-1]				
							item['state'] = addr[0].split(',')[-1].split()[-2]				
							item['city'] = " ".join(addr[0].split(',')[-1].split()[:-2])
							item['address'] = " ".join(addr[0].split(',')[:-1])
						else:
							item['zip_code'] = ""	
							item['state'] = addr[0].split(',')[-1].split()[-1]			
							item['city'] = addr[0].split(',')[-2].split()[-1]							
							item['address'] = " ".join(addr[0].split(',')[:-1]).replace(item['city'], '')
				except:
					pass
			else:
				if "," in addr[-1]:
					item['city'] = addr[-1].split(',')[0]
					item['state'] = " ".join(addr[-1].split(',')[-1].split()[:-1])
					item['zip_code'] = addr[-1].split(',')[-1].split()[-1]
					item['address'] = " ".join(addr[:-1])
				else:
					item['state'] = addr[-1].split()[-2]
					item['zip_code'] = addr[-1].split()[-1]
					try: 
						item['city'] = " ".join(addr[-1].split()[:-3])
						item['address'] = ",".join(addr[:-1])
					except:
						item['city'] = addr[-2]
						item['address'] = ",".join(addr[:-2])	
			if item['address'].strip()[-1] == ",":
				item['address'] = item['address'].strip()[:-1]			
			item['phone_number'] = self.validate(store.xpath('./p[2]/text()')).replace('.','-')
			hours = store.xpath('./p[3]/text()').extract()
			hours = [a.strip() for a in hours if a.strip() != ""]
			item['country'] = "United States"
			item['store_hours'] = ";".join(hours)
			item['latitude'] = self.validate(store.xpath('.//h1/a/@data-lat'))
			item['longitude'] = self.validate(store.xpath('.//h1/a/@data-lng'))
			item['other_fields'] = ""
			if "COMING SOON" in item['store_name']:
				item['coming_soon'] = 1
			else:
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
			return formatted_value
		except:
			return source