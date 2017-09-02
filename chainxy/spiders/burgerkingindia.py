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

class BurgerkingindiaSpider(scrapy.Spider):
		name = "burgerkingindia"
		uid_list = []
		start_urls = ['http://www.burgerkingindia.in/locations?field_geofield_distance[origin][lat]=19.0759&field_geofield_distance[origin][lon]=72.87765000000002']
		count = 0
		domain = "https://www.burgerking.com"

		def parse(self, response):
			try:
				page_count = int(response.xpath('//li[@class="pager-current"]/text()').extract_first().split("of ")[-1])
				for page_num in range(1, page_count+1):
					url = "http://www.burgerkingindia.in/locations?field_geofield_distance[origin][lat]=19.0759&field_geofield_distance[origin][lon]=72.87765000000002&page=" + str(page_num)
					yield scrapy.Request(url=url, callback=self.parse_page)				
			except:
				pass 

		def parse_page(self, response):
			for store in response.xpath("//div[@class='bk-restaurants']/ul/li"):
				item = ChainItem()
				item['store_number'] = self.validate(store.xpath('./div[@class="bk-id"]/text()').extract_first())
				item['store_name'] = self.validate(store.xpath('./div[@class="bk-location-title"]/text()').extract_first())
				item['address'] = self.validate(store.xpath('./div[@class="bk-address1"]/text()').extract_first())
				item['address2'] = ""
				item['city'] = self.validate(store.xpath('./div[@class="bk-city"]/text()').extract_first())
				item['state'] = self.validate(store.xpath('./div[@class="bk-state"]/text()').extract_first())
				item['zip_code'] = self.validate(store.xpath('./div[@class="bk-zip"]/text()').extract_first())
				item['country'] = self.validate(store.xpath('./div[@class="bk-country"]/text()').extract_first()) 
				item['phone_number'] = self.validate(store.xpath('./div[@class="bk-phone"]/text()').extract_first())
				item['store_hours'] = self.validate(store.xpath('./div[@class="bk-weekday-hours"]/text()').extract_first())
				item['latitude'] = self.validate(store.xpath('./div[@class="bk-latitude"]/text()').extract_first())
				item['longitude'] = self.validate(store.xpath('./div[@class="bk-longitude"]/text()').extract_first())
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = 0
				yield item
		
		def validate(self, str):
			if str == None:
				return ""
			return str.strip()
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
