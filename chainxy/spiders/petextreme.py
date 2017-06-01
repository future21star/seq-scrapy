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

class PetextremeSpider(scrapy.Spider):
		name = "petextreme"
		uid_list = []
		start_urls = ['http://www.petextreme.com/locations/']

		headers = {
			"X-Requested-With" : "XMLHttpRequest",
			"Content-Type": "application/x-www-form-urlencoded"
		}

		form_data = {
			"address": "",
			"formdata": "addressInput=",
			"lat": "37.09024",
			"lng": "-95.71289100000001",
			"name": "",
			"radius": "10000",
			"tags": "",
			"action": "csl_ajax_onload"
		}

		def start_requests(self):
			yield FormRequest(url="http://www.petextreme.com/wp-admin/admin-ajax.php", headers=self.headers, formdata=self.form_data, callback=self.parse_store)

		def parse_store(self, response):
			stores = json.loads(response.body)['response']
			for store in stores:
				item = ChainItem()
				item['store_number'] = store["id"]
				item['store_name'] = store["name"]
				item['address'] = store["address"]
				item['address2'] = store["address2"]
				item['city'] = store["city"]
				item['state'] = store["state"]
				item['zip_code'] = store["zip"]
				item['country'] = "United States" 
				item['phone_number'] = store["phone"]
				item['store_hours'] = store["hours"].replace("&#044", "").encode('utf8').replace('\xe2\x80\x93', '-')
				item['latitude'] = store["lat"]
				item['longitude'] = store["lng"]
				#item['store_type'] = info_json["@type"]
				item['coming_soon'] = 0
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




