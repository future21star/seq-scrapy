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

class OurcoopSpider(scrapy.Spider):
		name = "ourcoop"
		uid_list = []
		start_urls = ["http://www.ourcoop.com/ourcoop08/locator/allStores.aspx"]
		
		def start_requests(self):
			for state in self.us_state_abbrev:
				url = "http://www.landroverusa.com/national-dealer-locator.html?region=%s&filter=All" % self.us_state_abbrev[state]
				yield scrapy.Request(url=url, callback=self.parse_store)

		def parse_store(self, response):
			try:
				stores = response.xpath('//div[@class="infoCardDealer infoCard"]')
				for _store in stores:
					try:
						store = _store.xpath('.//div[@class="cardDetails clearfix"]')[0]
						item = ChainItem()
						item['store_number'] = ""
						item['store_name'] = self.validate(store.xpath('.//span[@class="dealerNameText"]/text()'))
						_addr = self.validate(store.xpath('.//tr[@class="address"]/td/text()'))
						addr = usaddress.parse(_addr.strip())
						item['address'] = item['address2'] = item['city'] = item['zip_code'] = item['state'] = ""
						for temp in addr:
							if temp[1] == 'PlaceName':
								item['city'] = temp[0].replace(',', '')
							elif temp[1] == 'StateName':
								item['state'] = temp[0].replace(',', '')
							elif temp[1] == 'ZipCode':
								item['zip_code'] = temp[0].replace(',', '')
						item['address'] = _addr.replace(',', '').replace(item['city'], '').replace(item['state'],'').replace(item['zip_code'],'').strip()								
						item['country'] = "United States"
						item['phone_number'] = self.validate(store.xpath('.//span[@class="itemTablet"]/text()'))
						item['store_hours'] = ""
						item['latitude'] = self.validate(_store.xpath('./@data-lat'))
						item['longitude'] = self.validate(_store.xpath('./@data-lng'))
						#item['store_type'] = info_json["@type"]
						item['other_fields'] = ""
						item['coming_soon'] = 0
						yield item
					except:
						pdb.set_trace()
						pass
			except:
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




