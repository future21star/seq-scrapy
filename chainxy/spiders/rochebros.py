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

class RochebrosSpider(scrapy.Spider):
		name = "rochebros"
		uid_list = []
		start_urls = ['http://www.rochebros.com/wp-admin/admin-ajax.php?action=do_ajax&fn=getLocations&search_loc_text=&location_text_filter=&caters=']

		def parse(self, response):
			stores = etree.HTML(response.body.replace('\\t','').replace('\\n','').replace('\\r', '').replace('\\', '')).xpath('//div[contains(@class, "box_margin_bottom")]')
			for store in stores:
				item = ChainItem()
				item['store_number'] = ""
				item['store_name'] = store.xpath('./h4[@class="font_16"]/text()')[0]
				addr = store.xpath('./p[1]/text()')
				addr = [a.strip() for a in addr if a.strip() != ""]
				item['address'] = " ".join(addr[:-1]).strip()
				item['address2'] = ""
				item['city'] = addr[-1].split(',')[0].strip()
				item['state'] = addr[-1].split(',')[1].split()[0].strip()
				item['zip_code'] = addr[-1].split(',')[1].split()[1].strip()
				item['country'] = "United States" 
				phone = store.xpath('./p[3]/text()')[0]
				item['phone_number'] = phone.split(":")[-1].strip().split('C')[0]
				hours = store.xpath('./p[2]//text()')
				hours = [a.strip() for a in hours if a.strip() != ""]
				item['store_hours'] = ""
				for hour in hours:
					if hours.index(hour) % 2 == 0:
						item['store_hours'] += hour
					else:
						item['store_hours'] += hour + ";"
				item['latitude'] = ""
				item['longitude'] = ""
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = 0
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




