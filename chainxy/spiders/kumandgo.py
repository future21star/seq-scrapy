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
import yaml

class KumandgoSpider(scrapy.Spider):
	name = "kumandgo"
	uid_list = []

	def start_requests(self):
		headers = {
			"accept":"*/*",
			"accept-encoding":"gzip, deflate, br",
			"accept-language":"en-US,en;q=0.8",
			"Content-Type":"application/x-www-form-urlencoded",
			"cookie":"ai_kng_locator=3.1097%7C101.6171; _ga=GA1.2.1664738755.1494572576; _gid=GA1.2.1592366791.1494572576; com.silverpop.iMAWebCookie=4e1b87ee-e4a4-7340-20db-de8327ca13dd; com.silverpop.iMA.page_visit=-1838907361:; com.silverpop.iMA.session=d5e34c32-7cba-a872-310b-316ed7d9226e; __ar_v4=%7CWQPY5DHCCBCDZMPBRQFGU4%3A20170511%3A1%7CT2OMBITPF5C4DPJDUTO53J%3A20170511%3A1%7CMCHAP2HK5VCL7LHD6WWLJB%3A20170511%3A1",
			"origin":"https://www.kumandgo.com",
			"referer":"https://www.kumandgo.com/find-a-store/?addressline=50266",
			"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
			"x-requested-with":"XMLHttpRequest"
		}
		form_data = {
			"action":"stores_coords",
			"coords[latitude]":"40.133096144299905",
			"coords[longitude]":"-93.79064516406248",
			"radius":"3000"
		}
		url = "https://www.kumandgo.com/wordpress/wp-admin/admin-ajax.php"
		yield FormRequest(url=url, formdata=form_data, callback=self.parse_store)

	def parse_store(self, response):
		try:
			stores = json.loads(response.body)["data"]["stores"]
			for store in stores:
				item = ChainItem()
				item['store_number'] = store["clientkey"]
				item['store_name'] = store["name"]
				item['address'] = store["address1"]
				item['address2'] = ""
				item['city'] = store["city"]
				item['state'] = store["state"]
				item['zip_code'] = store["postalcode"]
				item['latitude'] = store["latitude"]
				item['longitude'] = store["longitude"]
				item['country'] = store["country"]
				try:
					item['phone_number'] = store["kitchen_phone"].replace('{}', '')
				except:
					item['phone_number'] = ""
				item['store_hours'] = "Monday:" + store["monday_hours"] + ";" + "Tuesday:" + store["tuesday_hours"] + ";" + "Wednesday:" + store["wednesday_hours"] + ";" + "Thursday:" + store["thursday_hours"] + ";" + "Friday:" + store["friday_hours"] + ";" + "Saturday:" + store["saturday_hours"] + ";" + "Sunday:" + store["sunday_hours"] + ";"
				item['other_fields'] = ""
				item['coming_soon'] = 0
				yield item
		except:
			pdb.set_trace()
			pass            

