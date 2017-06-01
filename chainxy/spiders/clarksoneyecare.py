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
from lxml import etree
class ClarksoneyecareSpider(scrapy.Spider):
		name = "clarksoneyecare"
		uid_list = []
		start_urls = ["http://www.clarksoneyecare.com/locations/index.html"]
		domain = "http://www.clarksoneyecare.com"

		def parse(self, response):
			try:
				stores = response.xpath('//li[@class="block"]//a/@href').extract()
				for store in stores:
					url = self.domain + store
					yield scrapy.Request(url, callback=self.parse_store)
			except:
				pdb.set_trace()
				pass

		def parse_store(self, response):
			try:
				conf = json.loads(response.body.split("var config = ")[1].split("};")[0] + "}")
				url = "https://ws.bullseyelocations.com/RestLocation.svc/FormatLocation?ClientID=%s&ApiKey=%s&LocationID=%s&TemplateName=%s&theDataKeys=%s" % (conf["ClientID"], conf["ApiKey"], conf["LocationID"], conf["TemplateName"], conf["theDataKeys"].replace(":", "%3A"))
				request = scrapy.Request(url=url, callback=self.parse_detail)
				yield request
			except:
				pdb.set_trace()
				pass			

		def parse_detail(self, response):
			try:
				store = etree.HTML(response.body)
				item = ChainItem()
				item['store_number'] = ""
				item['store_name'] = ""
				addr = store.xpath('//div[@class="BE-Address BE-Component"]//text()')
				item['address'] = addr[0].strip()
				item['address2'] = ""
				try:
					item['city'] = addr[1].split(',')[0].strip()
					item['state'] = addr[1].split(',')[1].strip()
					item['zip_code'] = addr[1].split(',')[2].strip()
				except:
					item['city'] = addr[2].split(',')[0].strip()
					item['state'] = addr[2].split(',')[1].strip()
					item['zip_code'] = addr[2].split(',')[2].strip()					
				item['country'] = "United States" 
				if store.xpath('//div[@class="BE-Contact BE-Component"]/p//text()')[0].replace("Phone:", '').strip() != "":
					item['phone_number'] = store.xpath('//div[@class="BE-Contact BE-Component"]/p//text()')[0].replace('Phone:', '').strip()
				else:
					item['phone_number'] = store.xpath('//div[@class="BE-Contact BE-Component"]/p//text()')[1].replace('Phone:', '').strip()					
				hours = store.xpath('//div[@class="BE-Hours BE-Component"]//text()')
				hours = [a.strip() for a in hours if a.strip() != "" and ('Mon' in a or 'Tue' in a or 'Thu' in a or "Fri" in a or "Wed" in a or 'Sat' in a or 'Sun' in a)]
				item['store_hours'] = ";".join(hours).replace('Hours', '')
				item['other_fields'] = ""
				item['coming_soon'] = 0				
				lat_lng = response.body.split("maps.LatLng(")[1]
				item['latitude'] = lat_lng.split(',')[0].strip()
				item['longitude'] = lat_lng.split(',')[1].split(')')[0].strip()
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




