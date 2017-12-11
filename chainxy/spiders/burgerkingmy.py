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

class BurgerkingmySpider(scrapy.Spider):
		name = "burgerkingmy"
		uid_list = []
		start_urls = ['http://www.burgerking.com.my/Locator/Index?field_geofield_distance[origin][lat]=3.887809&field_geofield_distance[origin][lon]=108.18581199999994&page=1']
		count = 0
		domain = "https://www.burgerking.com"

		def parse(self, response):
			try:
				page_count = int(response.xpath('//li[@class="pager-current"]/text()').extract_first().split("of ")[-1])
				for page_num in range(1, page_count+1):
					url = "http://www.burgerking.com.my/Locator/Index?field_geofield_distance[origin][lat]=3.887809&field_geofield_distance[origin][lon]=108.18581199999994&page=" + str(page_num)
					yield scrapy.Request(url=url, callback=self.parse_page)				
			except:
				pass 

		def parse_page(self, response):
			for store in response.xpath("//div[@class='bk-restaurants']/ul/li"):
				item = ChainItem()
				item['store_number'] = self.validate(store.xpath('./div[@class="bk-num"]/text()').extract_first())
				item['store_name'] = self.validate(store.xpath('./div[@class="bk-title"]/text()').extract_first())
				item['zip_code'] = self.getZipCode(self.validate(store.xpath('./div[@class="bk-address1"]/text()').extract_first()))
				item['address'] = self.validate(store.xpath('./div[@class="bk-address1"]/text()').extract_first()).split(item['zip_code'])[0].strip()[:-1]
				item['address2'] = ""
				item['city'] = self.validate(store.xpath('./div[@class="bk-city"]/text()').extract_first())
				item['state'] = self.validate(store.xpath('./div[@class="bk-state"]/text()').extract_first())
				item['country'] = self.validate(store.xpath('./div[@class="bk-country"]/text()').extract_first()) 
				item['phone_number'] = self.validate(store.xpath('./div[@class="bk-phone"]/text()').extract_first())
				item['store_hours'] = self.validate(store.xpath('./div[@class="bk-operation_hours"]/text()').extract_first()).split("Operation Hours :")[-1].split("Operation Hours:")[-1].split("</p>")[0].split("</span>")[0].replace('&nbsp;','').replace('&ndash;','-').strip()
				item['latitude'] = self.validate(store.xpath('./div[@class="bk-latitude"]/text()').extract_first())
				item['longitude'] = self.validate(store.xpath('./div[@class="bk-longitude"]/text()').extract_first())
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = 0
				yield item
		
		def validate(self, str):
			if str == None:
				return ""
			return str
		def getZipCode(self, src):
			temps = src.replace(',',' ').replace('\r\n',' ').split(' ')
			while len(temps) != 0:
				temp = temps.pop()
				try:
					zipcode = int(temp)
					break
				except:
					continue
			return str(zipcode)

		
		
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

class BurgerkingmySpider(scrapy.Spider):
		name = "burgerkingmy"
		uid_list = []
		start_urls = ['http://www.burgerking.com.my/Locator/Index?field_geofield_distance[origin][lat]=3.887809&field_geofield_distance[origin][lon]=108.18581199999994&page=1']
		count = 0
		domain = "https://www.burgerking.com"

		def parse(self, response):
			try:
				page_count = int(response.xpath('//li[@class="pager-current"]/text()').extract_first().split("of ")[-1])
				for page_num in range(1, page_count+1):
					url = "http://www.burgerking.com.my/Locator/Index?field_geofield_distance[origin][lat]=3.887809&field_geofield_distance[origin][lon]=108.18581199999994&page=" + str(page_num)
					yield scrapy.Request(url=url, callback=self.parse_page)				
			except:
				pass 

		def parse_page(self, response):
			for store in response.xpath("//div[@class='bk-restaurants']/ul/li"):
				item = ChainItem()
				item['store_number'] = self.validate(store.xpath('./div[@class="bk-num"]/text()').extract_first())
				item['store_name'] = self.validate(store.xpath('./div[@class="bk-title"]/text()').extract_first())
				item['zip_code'] = self.getZipCode(self.validate(store.xpath('./div[@class="bk-address1"]/text()').extract_first()))
				item['address'] = self.validate(store.xpath('./div[@class="bk-address1"]/text()').extract_first()).split(item['zip_code'])[0].strip()[:-1]
				item['address2'] = ""
				item['city'] = self.validate(store.xpath('./div[@class="bk-city"]/text()').extract_first())
				item['state'] = self.validate(store.xpath('./div[@class="bk-state"]/text()').extract_first())
				item['country'] = self.validate(store.xpath('./div[@class="bk-country"]/text()').extract_first()) 
				item['phone_number'] = self.validate(store.xpath('./div[@class="bk-phone"]/text()').extract_first())
				item['store_hours'] = self.validate(store.xpath('./div[@class="bk-operation_hours"]/text()').extract_first()).split("Operation Hours :")[-1].split("Operation Hours:")[-1].split("</p>")[0].split("</span>")[0].replace('&nbsp;','').replace('&ndash;','-').strip()
				item['latitude'] = self.validate(store.xpath('./div[@class="bk-latitude"]/text()').extract_first())
				item['longitude'] = self.validate(store.xpath('./div[@class="bk-longitude"]/text()').extract_first())
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = 0
				yield item
		
		def validate(self, str):
			if str == None:
				return ""
			return str
		def getZipCode(self, src):
			temps = src.replace(',',' ').replace('\r\n',' ').split(' ')
			while len(temps) != 0:
				temp = temps.pop()
				try:
					zipcode = int(temp)
					break
				except:
					continue
			return str(zipcode)
