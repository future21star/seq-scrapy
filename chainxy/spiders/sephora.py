import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class SephoraSpider(scrapy.Spider):
		name = "sephora"
		uid_list = []

		headers = { "Content-Type": "application/json", "Accept":"*/*" }

		def __init__(self):
			place_file = open('all_code_list.csv', 'rb')
			self.place_reader = csv.reader(place_file)

		def start_requests(self):
			for row in self.place_reader:
				request_url = "http://www.sephora.com/about/storeresults.jsp?lng=%s&lat=%s&loc=%s&radius=5&unit=miles" % (row[2], row[1], row[0])
				yield scrapy.Request(url=request_url, callback=self.parse_store)

    # get longitude and latitude for a state by using google map.
		def parse_store(self, response):
			# try:
			try:
				pdb.set_trace()
				stores = response.xpath('//div[contains(@class,"StoreResult")]')
				for store in stores:
					item = ChainItem()
					item['store_name'] = self.replaceWithNone(store.xpath("./strong/a/text()").extract()[0])
					item['store_number'] = self.replaceWithNone(store.xpath("./strong/a/text()").extract()[1])
					item['address'] = self.replaceWithNone(store.xpath('./text()').extract()[1]) 
					item['address2'] = ""
					item['phone_number'] = self.replaceWithNone(store.xpath('./text()').extract()[3])
					item['city'] = self.replaceWithBlank(store.xpath('./text()').extract()[2]).split()[0]
					item['state'] = self.replaceWithBlank(store.xpath('./text()').extract()[2]).split()[1]
					item['zip_code'] = self.replaceWithBlank(store.xpath('./text()').extract()[2]).split()[2]
					item['country'] = ""
					item['latitude'] = ""
					item['longitude'] = ""
					item['store_hours'] = ""
					# item['store_type'] = info_json["@type"]
					item['other_fields'] = ""
					item['coming_soon'] = ""
					if item['store_number'] == "" or (item["store_number"] in self.uid_list):
					    return
					self.uid_list.append(item["store_number"])
					yield item
			except:
				pass

		def validate(self, xpath_obj):
			try:
				return xpath_obj.extract_first().strip()
			except:
				return ""

		def replaceWithNone(self, str):
			try:
				return str.replace('\r', '').replace('\n','').replace('\t','')
			except:
				return ""
		def replaceWithBlank(self, str):
			try:
				return str.replace('\r', ' ').replace('\n',' ').replace('\t',' ').replace(',', ' ')
			except:
				return ""			