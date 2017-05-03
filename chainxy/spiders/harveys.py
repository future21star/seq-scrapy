import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class HarveysSpider(scrapy.Spider):
	name = "harveys"
	uid_list = []
	start_urls = ["https://www.harveys.ca/eng/locations?province_val=mb&city_val=Winnipeg&imageField.x=226&imageField.y=15"]
		
	def parse(self, response):
		try:
			markers = response.xpath('//script/text()').extract_first()
			markers = markers[markers.find("createMarker(new") + 16: -1]
			pos = 0;
			while markers.index('location_map.php',pos, -1) > -1:
				pos = markers.index('location_map.php', pos, -1)
				url = ""
				while markers[pos] != "'":
					url += markers[pos]
					pos += 1
				store_number = url[url.find("id=")+3:]
				item = ChainItem()
				item['store_number'] = store_number
				url = url.replace(".php", "")
				url = "https://www.harveys.ca/eng/" + url
				request = scrapy.Request(url = "https://www.harveys.ca/eng/location_map?id=1345", callback=self.parse_store)
				request.meta['item'] = item
				yield request
		except:
			pass

	def parse_store(self, response):
		try:
			item = response.meta['item']
			stores = response.xpath('//span[@class="tx_grey_3"]').extract_first()
			pos = response.body.index('class="tx_grey_3"') + 18 
			item['address'] = item['city'] = item['state'] = item['zip_code'] = item['store_hours'] = item['phone_number'] = ''
			while response.body[pos] != ',':
				item['address'] += response.body[pos]
				pos += 1
			item['address'] = self.replaceUnknownLetter(item['address'])
			pos += 1
			while response.body[pos] != ',':
				item['city'] += response.body[pos]
				pos += 1
			pos += 1
			while response.body[pos] != ',':
				item['state'] += response.body[pos]
				pos += 1
			pos += 1
			while response.body[pos] != '<':
				item['zip_code'] += response.body[pos]
				pos += 1
			item['zip_code'] = item['zip_code'].strip()
			pos += 1
			pos = response.body.index('Hours...</strong><br>') + 21
			while response.body[pos: pos+6] != '<br><s':
				item['store_hours'] += response.body[pos]
				pos += 1
			item['store_hours'] = item['store_hours'].strip()
			item['store_hours'] = item['store_hours'].replace('<br>', ';')
			pos = response.body.index("Phone:</strong>") + 15
			while response.body[pos] != '<':
				item['phone_number'] += response.body[pos]
				pos += 1
			item['phone_number'] = item['phone_number'].strip()
			
			pos = response.body.index("setCenter(new GLatLng(") + 22
			item['latitude'] = ""
			while response.body[pos] != ',':
				item['latitude'] += response.body[pos]
				pos += 1
			item['latitude'] = item['latitude'].strip()
			item['longitude'] = ""
			pos += 1
			while response.body[pos] != ')':
				item['longitude'] += response.body[pos]
				pos += 1
			item['longitude'] = item['longitude'].strip()
			item['other_fields'] = ""
			item['coming_soon'] = 0
			if item['phone_number'] == "" or item['phone_number'] in self.uid_list:
				return
			self.uid_list.append(item['phone_number'])
			yield item
		except:
			pass

	def validate(self, xpath):
		try:
			return xpath.extract_first().strip()
		except:
			return ""

	def validate_with_index(self, xpath, index):
		try:
			return xpath.extract()[index]
		except:
			return ""

	def replaceUnknownLetter(self, source):
		try:
			formatted_value = source.replace('\xc3', '').replace('\xe9', 'e').replace('\xe8', 'e').replace('\xe4', 'o').replace('\xe3', 'o').replace('\xe9', 'u').replace('\xea', 'u').replace('\x89', 'E').replace('\xaa', 'e').replace('\x89', 'E').replace('\xa2', 'a').replace('\xac', 'i').replace('\xad', 'i').replace('\xae', 'i')
			# if "x8" in formatted_value or "x9" in formatted_value or "xa" in formatted_value or "xb" in formatted_value:
			# 	pdb.set_trace()
			return formatted_value
		except:
			return source
