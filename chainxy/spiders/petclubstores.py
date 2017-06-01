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
import usaddress
from lxml import etree

class PetclubstoresSpider(scrapy.Spider):
		name = "petclubstores"
		uid_list = []
		start_urls = ['https://www.petclubstores.com/locations-1/']

		def parse(self, response):
			stores = response.xpath('//div[@class="col sqs-col-3 span-3"]/div[@class="sqs-block html-block sqs-block-html"]')
			for store in stores:
				item = ChainItem()
				item['store_number'] = ""
				addr = store.xpath('.//div[@class="sqs-block-content"]/p[1]//text()').extract()
				item['store_name'] = addr[0].split('-')[0].strip()
				item['coming_soon'] = 0
				if 'Coming Soon' in addr[0]:
					item['coming_soon'] = 1
				item['address'] = addr[1].strip()
				item['address2'] = ""
				item['city'] = addr[2].split(',')[0].strip()
				item['state'] = addr[2].split(',')[1].split()[0].strip()
				item['zip_code'] = addr[2].split(',')[1].split()[1].strip()
				item['country'] = "United States" 
				phone = self.validate(store.xpath('.//div[@class="sqs-block-content"]/p[2]//text()'))
				item['phone_number'] = phone.split(":")[-1].strip().replace('coming soon', '').strip()
				hours = response.xpath('//div[@class="col sqs-col-12 span-12"]/div[1]/div[1]/p[1]/strong[2]/text()').extract()
				item['store_hours'] = ";".join(hours)
				lat_lng = response.xpath("//a[contains(@href, 'https://www.google.com/maps/')]/@href").extract()[stores.index(store)]
				item['latitude'] = lat_lng.split("@")[-1].split(',')[0]
				item['longitude'] = lat_lng.split("@")[-1].split(',')[1].split(',')[0]
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				yield item		
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




