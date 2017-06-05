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

class PeerlesstyrecoSpider(scrapy.Spider):
		name = "peerlesstyreco"
		uid_list = []
		start_urls = ["http://www.peerlesstyreco.com/peerless-tires-store-locations.php"]
			
		def parse(self, response):
			states = response.xpath('//span[@class="view-locs"]/a[1]/@href').extract()
			for state in states:
				url = "http://www.peerlesstyreco.com/" + state
				yield scrapy.Request(url=url, callback=self.parse_store)

		def parse_store(self, response):
			try:
				stores = response.xpath('//ul[@id="state_totals"]/li')
				for store in stores:
					if stores.index(store) > 0:
						item = ChainItem()
						item['store_number'] = ""
						item['store_name'] = self.validate(store.xpath('.//h5[@class="store-results-count"]/a/text()'))
						item['store_type'] = ""
						item['address'] = self.validate(store.xpath('./text()'))
						item['address2'] = ""
						_addr = store.xpath('./text()').extract()[1]
						item['city'] = item['state'] = item['zip_code'] = ""
						addr = usaddress.parse(_addr.strip())
						for temp in addr:
							if temp[1] == 'PlaceName':
								item['city'] += temp[0].replace(',', '')
							elif temp[1] == 'StateName':
								item['state'] = temp[0].replace(',', '')
							elif temp[1] == 'ZipCode':
								item['zip_code'] = temp[0].replace(',', '')

						item['country'] = "United States"
						item['phone_number'] = store.xpath('./text()').extract()[2].strip()
						hours = response.xpath('//div[@class="text-left"]/text()').extract()
						hours = [a.strip() for a in hours if a.strip() != ""]
						item['store_hours'] = ";".join(hours[1:])
						lat_lng = self.validate(store.xpath('.//a[contains(@href, "https://maps.google.com/maps?")]/@href'))
						item['latitude'] = lat_lng.split('q=')[1].split(',')[0]
						item['longitude'] = lat_lng.split('q=')[1].split(',')[1]
						item['other_fields'] = ""
						item['coming_soon'] = 0
						yield item
			except:
				pass			

		def validate(self, xpath):
			try:
				return self.replaceUnknownLetter(xpath.extract_first().strip())
			except:
				return ""

		def isOne(self, _str):
			try:
				return int(_str.split('(')[1].split(')')[0]) == 1
			except:
				return False;
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




