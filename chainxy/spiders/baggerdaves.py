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

class BaggerdavesSpider(scrapy.Spider):
		name = "baggerdaves"
		uid_list = []
		start_urls = ['https://www.baggerdaves.com/locations/']
		domain = 'https://www.baggerdaves.com/'
		domain1 = 'https://google.com'
		
		def parse(self, response):
			try:
				stores = yaml.load((response.body.split("NearestPosts = ")[-1].split("};")[0] + "}").replace('\\/', ''))["posts"]
				for store in stores:
					item = ChainItem()
					item['store_number'] = ""
					item['store_name'] = store['post_title']
					item['address'] = store['address']
					item['address2'] = ""
					item['city'] = store['city']
					item['state'] = store['state']
					item['zip_code'] = store['zipcode']
					item['country'] = "United States"
					item['phone_number'] = store['phone'].replace('.','-')
					hours = store['hours']
					item['store_hours'] = ""
					for hour in hours:
						item['store_hours'] += hour["days"] + ":" + hour["hours"] + ";"
					item['latitude'] = store['latitude']
					item['longitude'] = store['longitude']
					#item['store_type'] = info_json["@type"]
					item['other_fields'] = ""
					item['coming_soon'] = 0
					yield item
			except:
				pass
		def validate(self, xpath):
			try:
				return xpath.extract_first().strip()
			except:
				return ""
		def replaceUnknownLetter(self, source):
			try:
				formatted_value = source.encode('utf8').replace('\xc3', '').replace('\xa9', 'e').replace('\xa8', 'e').replace('\xb4', 'o').replace('\xb3', 'o').replace('\xb9', 'u').replace('\xba', 'u').replace('\x89', 'E').replace('\xaa', 'e').replace('\x89', 'E').replace('\xa2', 'a').replace('\xac', 'i').replace('\xad', 'i').replace('\xae', 'i')
				return formatted_value
			except:
				return source

