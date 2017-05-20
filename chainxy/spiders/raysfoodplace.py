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

class RaysfoodplaceSpider(scrapy.Spider):
		name = "raysfoodplace"
		uid_list = []
		start_urls = ['http://www.gorays.com/StoreLocator/Store_MapLocation_S.las?State=all']

		def parse(self, response):
			stores = json.loads(response.body)
			for store in stores:
				item = ChainItem()
				item['store_number'] = store['StoreNbr']
				item['latitude'] = store['Latitude']
				item['longitude'] = store['Longitude']
				url = "http://www.gorays.com/StoreLocator/Store_Detail_S.las?L=" + item['store_number']
				request = scrapy.Request(url=url, callback=self.parse_store)
				request.meta['item'] = item
				yield request
		def parse_store(self, _store):
			item = _store.meta['item']
			store = _store.xpath('//div[@class="col-md-9"]')
			item['store_name'] = self.validate(store.xpath('./h3/text()'))
			_temp = etree.HTML(_store.body.replace('<div class="address_wrapper"', '<div class="address_wrapper">'))
			addr = _temp.xpath('//p[@class="Address"]/text()')
			addr = [a.strip() for a in addr if a.strip() != ""]
			item['address'] = addr[0].strip()
			item['address2'] = ""
			item['city'] = addr[1].strip().split(',')[0]
			item['state'] = addr[1].strip().split(',')[1].split()[0]
			item['zip_code'] = addr[1].strip().split(',')[1].split()[1]
			item['country'] = "United States" 
			item['phone_number'] = self.validate(store.xpath('.//p[@class="PhoneNumber"]/text()'))
			item['store_hours'] = self.validate(store.xpath('.//table[@id="hours_info-BS"]//dd[1]/text()'))
			#item['store_type'] = info_json["@type"]
			item['other_fields'] = ""
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




