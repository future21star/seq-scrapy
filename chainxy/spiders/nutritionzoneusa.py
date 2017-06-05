import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb
import usaddress
import unicodedata

class NutritionzoneusaSpider(scrapy.Spider):
		name = "nutritionzoneusa"
		uid_list = []
		start_urls = ['https://www.nutritionzoneusa.com/Store-Locator']
		count = 0

		def parse(self, response):
			try:
				stores = response.xpath('//div[@class="service-info"]')
				body = response.body
				lat_lng = []
				while body.find("LatLng(") >= 0:
					pos = body.find("LatLng(")
					lat_lng.append(
						{
							"lat": body.split("LatLng(")[1].split(',')[0].strip(),
							"lng": body.split("LatLng(")[1].split(',')[1].split(')')[0].strip()
						}
					)
					body = "LatLng(".join(body.split("LatLng(")[1:])
				for store in stores:
					item = ChainItem()
					item['store_number'] = ""
					item['store_name'] = self.validate(store.xpath('./span[@class="service-name"]/text()'))
					_addr = self.validate(store.xpath('.//span[@class="service-description"][3]/text()'))
					if 'Address' in _addr:
						_addr = self.validate(store.xpath('.//span[@class="service-description"][4]/text()'))

					addr = usaddress.parse(_addr.strip())
					item['city'] = item['state'] = item['zip_code'] = ""
					for temp in addr:
						if temp[1] == 'PlaceName':
							item['city'] += temp[0].replace(',','')
						elif temp[1] == 'StateName':
							item['state'] += temp[0].replace(',','')
						elif temp[1] == 'ZipCode':
							item['zip_code'] = temp[0].replace(',','')							
					item['address'] = _addr.replace(',', '').replace(item['city'], '').replace(item['state'],'').replace(item['zip_code'],'').strip()
					item['address2'] = ''
					# if 'St' in addr[-2]:
					# 	item['address'] = " ".join(addr[:-2]).strip()
					# else:
					# 	item['address'] = " ".join(addr[:1]).strip()
					# item['address2'] = ""
					# item['city'] = addr[0].split()[-1].strip()
					# item['state'] = addr[1].split()[0].strip()
					# item['zip_code'] = addr[1].split()[1].strip()
					item['country'] = "United States" 
					item['phone_number'] = self.validate(store.xpath('.//span[@class="service-description"][6]/text()')).replace('N/A', '').replace('Phone', '').replace(':', '').strip()
					if item['phone_number'] == "":
						item['phone_number'] = self.validate(store.xpath('.//span[@class="service-description"][5]/text()')).replace('N/A', '').replace('Phone', '').replace(':', '').strip()
					# if item['store_name'] == "NUTRITION ZONE FOOTHILL RANCH":
					# 	pdb.set_trace()
					if "Monday" in self.validate(store.xpath('.//span[@class="service-description"][10]/text()')):
						item['store_hours'] = self.validate(store.xpath('.//span[@class="service-description"][10]/text()')) + ";" + self.validate(store.xpath('.//span[@class="service-description"][11]/text()')) + ";" + self.validate(store.xpath('.//span[@class="service-description"][12]/text()')) + ";" + self.validate(store.xpath('.//span[@class="service-description"][13]/text()'))	+ ";"				
						item['store_hours'] = item['store_hours'].replace('Friday- ', 'Friday:').replace('Sunday-', 'Sunday:').replace('Monday- Thursday ', 'Monday-Thursday:')
					else:
						item['store_hours'] = self.validate(store.xpath('.//span[@class="service-description"][8]/text()')).replace('Hours Open today', '')[3:].strip().encode('utf8').replace('\xe2\x80\x93', '-')
					if item['store_hours'] == "":
						item['store_hours'] = self.validate(store.xpath('.//span[@class="service-description"][7]/text()')).replace('Hours Open today', '')[3:].strip().encode('utf8').replace('\xe2\x80\x93', '-')	
					if item['store_hours'] == "" or ("am" not in item['store_hours'] and 'Monday' not in item['store_hours']):
						item['store_hours'] = self.validate(store.xpath('.//span[@class="service-description"][9]/text()')).replace('Hours Open today', '')[3:].strip().encode('utf8').replace('\xe2\x80\x93', '-')
					item['latitude'] = lat_lng[stores.index(store)]["lat"]
					item['longitude'] = lat_lng[stores.index(store)]["lng"]
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

		def isPhoneNumber(self, str):
			str = str.replace('(', '').replace(')', '').replace('-', '').replace('-', '').replace(' ','').replace('.', '').strip()
			count = 0
			for char in str:
				if not char.isdigit():
					return False
			return True
