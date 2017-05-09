import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class ManchuworkSpider(scrapy.Spider):
	name = "manchuwork"
	uid_list = []

	def start_requests(self):
		form_data = {
			"lat": "37.09024",
			"lng": "-95.71289100000001",
			"radius": "10000",
			"action": "csl_ajax_onload",
			"formdata": "addressInput="
		}
		request = FormRequest(url="https://manchuwok.com/wp-admin/admin-ajax.php", formdata=form_data, callback=self.parse_store)
		yield request

	def parse_store(self, response):
		stores = json.loads(response.body)["response"]
		for store in stores:
			item = ChainItem()
			item['store_number'] = store["id"]
			item['store_name'] = store["name"]
			item['address'] = store["address"]
			item['address2'] = store["address2"]
			item['phone_number'] = store["phone"]
			item['city'] = store["city"]
			item['state'] = store["state"]
			item['country'] = store["country"]
			item['latitude'] = store["lat"]
			item['longitude'] = store["lng"]
			#item['store_type'] = info_json["@type"]
			item['other_fields'] = ""
			item['coming_soon'] = 0
			item['zip_code'] = store["zip"]
			item['store_hours'] = store["hours"]
			yield item

	def validate(self, xpath_obj):
		try:
			return xpath_obj.extract_first().strip().encode('utf8').replace('\xc3\xb4', 'o').replace("&#39", "'").replace('&amp;nbsp;', '').replace('&nbsp;', '')
		except:
			return ""

	def hasNumbers(self, str):
		return any(char.isdigit() for char in str)
