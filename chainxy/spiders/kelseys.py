import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class KelseysSpider(scrapy.Spider):
	name = "kelseys"
	uid_list = []
	start_urls = ["http://www.kelseys.ca/location_region.php"]
	count = 0
	def parse(self, response):
		try:
			states = response.xpath('//select[@id="province"]/option')
			for state in states:
				if states.index(state) > 0:
					state_val = state.xpath('./@value').extract_first()
					item = ChainItem()
					item['state'] = state_val
					url = "http://www.kelseys.ca/location_get_city_loc.php?province=%s" % state_val
					request = scrapy.Request(url=url, callback=self.parse_state)
					request.meta['item'] = item
					yield request
		except:
			pdb.set_trace()
			pass

	def parse_state(self, response):
		try:
			cities = response.xpath('//select[@class="locatorSelect"]/option')
			for city in cities:
				if cities.index(city) > 0:
					city_value = city.xpath('./@value').extract_first()
					item = response.meta['item']
					item['city'] = city_value
					url = "http://www.kelseys.ca/location_region.php?province=%s&s=1&city_drop=%s" % (item['state'], item['city'])
					request = scrapy.Request(url=url, callback=self.parse_store)
					request.meta['item'] = item
					yield request
		except:
			pdb.set_trace()
			pass

	def parse_store(self, response):
		try:
			item = response.meta['item']
			if item['city'] == "Barrie":
				pdb.set_trace()
			stores = response.xpath('//ul[@id="thumbs"]')[0].xpath('./li')
			if len(stores) > 1:
				pdb.set_trace()

			for store in stores:
				info = store.xpath('.//div[@class="one"]')[0]
				item['store_number'] = ""
				item['store_name'] = ""
				item['address'] = info.xpath('./span[1]/text()').extract()[1].strip()
				item['address2'] = ""
				item['city'] = ",".join(self.validate(info.xpath('./p[1]/text()')).split(',')[:-2]).strip()
				item['state'] = self.validate(info.xpath('./p[1]/text()')).split(',')[-2].strip()
				item['zip_code'] = self.validate(info.xpath('./p[1]/text()')).split(',')[-1].strip()
				item['country'] = "Canada" 
				item['phone_number'] = self.validate(info.xpath('./p[1]/strong[1]/a[1]/text()')).split(':')[-1].strip()
				item['store_hours'] = ""
				item['latitude'] = self.validate(info.xpath('./p[2]/a[1]/img/@src')).split('=')[-1].split(',')[0]
				item['longitude'] = self.validate(info.xpath('./p[2]/a[1]/img/@src')).split('=')[-1].split(',')[1]
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = 0
				self.count += 1
				print self.count
				yield item
		except:
			pdb.set_trace()
			pass

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
