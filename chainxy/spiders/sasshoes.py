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

class SasshoesSpider(scrapy.Spider):
		name = "sasshoes"
		uid_list = []

		def parse(self, response):
			try:
				for state in response.xpath("//div[@class='locationCities']/a/@href").extract():					
					url = self.domain + state
					yield scrapy.Request(url=url, callback=self.parse_store)
			except:
				pdb.set_trace()
				pass
		def parse_store(self, response):
			try:
				stores = yaml.load(response.body.split("var locationListFC = '")[-1].split("}]}")[0] + "}]}")['locationData']
				stores += yaml.load(response.body.split("var locationListATM = '")[-1].split("}]}")[0] + "}]}")['locationData']
				self.count += len(stores)
				print "------------------------store count-----------------------------"
				print self.count
				print "------------------------store count-----------------------------"
				for store in stores:

					item = ChainItem()
					item['store_number'] = store['LocationID']
					item['store_name'] = store['Title']
					item['address'] = store['Address']
					item['address2'] = ""
					addr = store['CityStateZip']
					item['city'] = addr.split(',')[0].strip()
					item['state'] = addr.split(',')[-1].split()[0].strip()
					item['zip_code'] = addr.split(',')[-1].split()[1].strip()
					item['country'] = "United States" 
					item['phone_number'] = store['Phone'].replace('.', '-')
					item['store_hours'] = ""
					item['latitude'] = store['Latitude']
					item['longitude'] = store['Longitude']
					#item['store_type'] = info_json["@type"]
					item['other_fields'] = ""
					item['coming_soon'] = 0
					url = 'https://www.frostbank.com/pages/locationsdetail.aspx?LocationID=%s' % store['LocationID']
					request = scrapy.Request(url=url, callback=self.parse_hour)
					request.meta['item'] = item
					yield request
			except:
				pass			

		def parse_hour(self, response):
			try:
				store = yaml.load(response.body.split("var locationList = '")[-1].split('},]}')[0] + '},]}')['locationData'][0]
				item = response.meta['item']
				item['store_hours'] = store['LobbyHour']
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




