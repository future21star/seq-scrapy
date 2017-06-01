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
class WarbyparkerSpider(scrapy.Spider):
		name = "warbyparker"
		uid_list = []
		start_urls = ["https://www.warbyparker.com/retail"]
		domain = "https://www.warbyparker.com"

		def parse(self, response):
			try:
				keyword = '"\\/api\\/v2\\/retail\\/locations":'
				stores = json.loads(response.body.split(keyword)[1].split(',"\/api\/v2\/variations\/retail\/locations"')[0])["locations"]
				for store in stores:
					item = ChainItem()
					item['store_number'] = ""
					item['store_name'] = store["name"]
					item['address'] = store["address"]["street_address"]
					item['address2'] = ""
					item['city'] = store["address"]["locality"]
					item['state'] = store["address"]["region_code"]
					item['zip_code'] = store['address']['postal_code']
					item['country'] = store['address']['country_code']
					item['phone_number'] = store["cms_content"]["phone"].replace('.', '-')
					hours = store["schedules"][0]["hours"]
					days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
					item['store_hours'] = ""
					for day in days:
						try:
							item['store_hours'] += day + ":" + hours[day]['open'] + "-" + hours[day]['close'] + ";"
						except:
							if hours[day]['closed']:
								item['store_hours'] += day + ":closed" + ";"
					item['latitude'] = store['cms_content']["map_details"]['latitude']
					item['longitude'] = store['cms_content']["map_details"]['longitude']
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




