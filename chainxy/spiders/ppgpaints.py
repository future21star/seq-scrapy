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
from lxml import etree

class PpgpaintsSpider(scrapy.Spider):
	name = "ppgpaints"
	uid_list = []
	start_urls = ['https://www.ppgpaints.com/store-locator/countries']
	domain = "https://www.ppgpaints.com"

	def parse(self, response):
		countries = response.xpath('//a[contains(@href,"/store-locator/")]')
		for country in countries:
			if country.xpath('./@title').extract_first().strip() in ['United States', 'Canada']:
				country_url = self.domain + country.xpath('./@href').extract_first()
				request = scrapy.Request(url = country_url, callback=self.parse_country)
				item = ChainItem()
				item['country'] = country.xpath('./@title').extract_first().strip()
				request.meta['item'] = item
				yield request

	def parse_country(self, response):
	  	states = response.xpath('//a[contains(@href,"/store-locator/")]')
	  	for state in states:
	   		state_url = self.domain + state.xpath('./@href').extract_first()
	  		request = scrapy.Request(url = state_url, callback=self.parse_state)
	  		item = response.meta['item']
	  		item['state'] = state.xpath('./@text').extract_first()
	  		request.meta['item'] = item
	  		yield request

	def parse_state(self, response):
	  	cities = response.xpath('//ul[@class="clarityCol"]/li/a')
	  	for city in cities:
	  		city_url = self.domain + city.xpath('./@href').extract_first()
	  		request = scrapy.Request(url = city_url, callback=self.parse_store)
	  		item = response.meta['item']
	  		item['city'] = city.xpath('./@text').extract_first()
	  		request.meta['item'] = item
	  		yield request

	def parse_store(self, response):
		item = response.meta['item']
		stores = response.xpath('//div[@class="clarityResults resultsContainer"]/ul/li')
		for store in stores:
			item['store_number'] = ""
			item['store_name'] = self.validate(store.xpath('.//span[@itemprop="name"]/text()'))
			item['address'] = self.validate(store.xpath('.//span[@itemprop="streetAddress"]/text()'))
			item['address2'] = ""
			item['city'] = self.validate(store.xpath('.//span[@itemprop="addressLocality"]/text()')).strip()[:-1]
			item['state'] = self.validate(store.xpath('.//span[@itemprop="addressRegion"]/text()'))
			item['zip_code'] = self.validate(store.xpath('.//span[@itemprop="postalCode"]/text()'))
			item['phone_number'] = self.validate(store.xpath('.//span[@itemprop="telephone"]/a/text()'))
			item['store_hours'] = ""
			lat_lng = self.validate(store.xpath('.//div[@class="cta-text-container"]/p[1]/a[1]/@href')).split("sll=")[-1]
			item['latitude'] = lat_lng.split(',')[0]
			item['longitude'] = lat_lng.split(',')[-1]
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
			return formatted_value
		except:
			return source