import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class HurricanewingsSpider(scrapy.Spider):
	name = "hurricanewings"
	uid_list = []
	start_urls = ["http://www.hurricanewings.com/locations/"]
	count = 0

	def parse(self, response):
		# try:
		stores = response.xpath('//div[@class="locations-list"]/div')
		for store in stores:
			item = ChainItem()
			item['store_number'] = ""
			item['store_name'] = ""
			item['address'] = store.xpath('./div[@class="address third"]/text()').extract()[0].strip()
			item['address2'] = ""
			addr = store.xpath('./div[@class="address third"]/text()').extract()
			addr = [a.strip() for a in addr if a.strip() != ""]
			item['city'] = addr[-1].strip().split(',')[0].strip()
			item['state'] = addr[-1].strip().split(',')[1].strip().split()[0]
			item['zip_code'] = addr[-1].strip().split(',')[1].strip().split()[1]
			item['country'] = "United States" 
			item['phone_number'] = store.xpath('./div[@class="title"]/text()').extract()[1].strip()
			hours = store.xpath('.//div[@class="hours third"]/text()').extract()
			hours = [a.strip() for a in hours if a.strip() != ""]
			item['store_hours'] = ";".join(hours)
			lat_lng = store.xpath('./@data-click').extract_first()
			item['latitude'] = lat_lng[:-1].split(',')[-2].strip()
			item['longitude'] = lat_lng[:-1].split(',')[-1].strip()
			#item['store_type'] = info_json["@type"]
			item['other_fields'] = ""
			item['coming_soon'] = 0
			if "COMING SOON" in "".join(store.xpath('./div[@class="title"][1]//text()').extract()):
				item['coming_soon'] = 1
			yield item
		# except:
		# 	pdb.set_trace()
		# 	pass

	def validate(self, xpath):
		# try:
		return xpath.extract_first().strip()
		# except:
			# return ""

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
