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

class AgrisupplySpider(scrapy.Spider):
		name = "agrisupply"
		uid_list = []
		start_urls = ['http://www.agrisupply.com/']

		def parse(self, response):
			for store in response.xpath("//ul[@class='nav nav-pills nav-main']/li[5]/ul[1]/li/a/@href").extract():					
				url = "http://www.agrisupply.com" + store
				item = ChainItem()
				item['store_number'] = store.split('/')[-2]
				request = scrapy.Request(url=url, callback=self.parse_store)
				request.meta['item'] = item
				yield request

		def parse_store(self, store):
				item = store.meta['item']
				item['store_name'] = self.validate(store.xpath('//section[@class="page-header"]/div[@class="container"]/div[2]/div[1]/h1/text()'))
				addr = store.xpath('//ul[@class="list list-icons list-icons-style-3 mt-xlg"]/li[1]/text()').extract()
				item['address'] = addr[0].strip()
				item['address2'] = ""
				item['city'] = addr[1].split(',')[0].strip()
				item['state'] = addr[1].split(',')[1].split()[0]
				item['zip_code'] = " ".join(addr[1].split(',')[1].split()[1:])
				item['country'] = "United States" 
				item['phone_number'] = store.xpath('//ul[@class="list list-icons list-icons-style-3 mt-xlg"]/li[2]/text()').extract()[0].strip()
				hours = store.xpath('//ul[@class="list list-icons list-dark mt-xlg"]//text()').extract()
				hours = [a.strip() for a in hours if a.strip() != ""]
				item['store_hours'] = ";".join(hours)
				item['latitude'] = store.body.split("ll=")[-1].split(',')[0]
				item['longitude'] = store.body.split("ll=")[-1].split(',')[1].split('&')[0]
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = 0
				yield item		

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




