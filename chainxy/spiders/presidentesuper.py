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

class PresidentesuperSpider(scrapy.Spider):
		name = "presidentesuper"
		uid_list = []
		start_urls = ['http://presidentesupermarkets.com/location/']

		def parse(self, response):
			pages = len(response.xpath('//a[contains(@href, "http://presidentesupermarkets.com/location/page/")]'))
			for page in range(pages):
				url = "http://presidentesupermarkets.com/location/page/" + str(page + 1)
				yield scrapy.Request(url=url, callback=self.parse_store)

		def parse_store(self, response):
			pos = 0
			for store in response.xpath('//ul[@class="maplist"]/li/div'):
				try:
					item = ChainItem()
					item['store_number'] = self.validate(store.xpath('./@id')).split('-')[-1]
					item['store_name'] = self.validate(store.xpath('./div[@class="entry"]/h2/text()'))
					_addr = store.xpath('./div[@class="entry"]/p/text()').extract()
					item['address'] = _addr[0].strip()
					item['address2'] = ""
					addr = usaddress.parse(_addr[1].strip())
					item['city'] = item['state'] = item['zip_code'] = ""
					for temp in addr:
						if temp[1] == 'PlaceName':
							item['city'] += temp[0].replace(',','') + ' '
						elif temp[1] == 'StateName':
							item['state'] += temp[0].replace(',','') + ' '
						elif temp[1] == 'ZipCode':
							item['zip_code'] = temp[0].replace(',','')						
					item['country'] = "United States" 
					item['phone_number'] = self.validate(store.xpath('.//span[@class="phone"]/text()'))
					item['store_hours'] = self.validate(store.xpath('.//span[@class="hours"]/text()'))
					start_pos = response.body.find('google.maps.LatLng("', pos) + 20
					end_pos = response.body.find('")', start_pos)
					lat_lng = response.body[start_pos: end_pos]
					if lat_lng != "":
						item['latitude'] = lat_lng.split('",')[0].strip()
						item['longitude'] = lat_lng.split('", "')[-1].strip()
					else:
						item['latitude'] = ""
						item['longitude'] = ""
					pos = end_pos + 1
					#item['store_type'] = info_json["@type"]
					item['other_fields'] = ""
					item['coming_soon'] = 0
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




