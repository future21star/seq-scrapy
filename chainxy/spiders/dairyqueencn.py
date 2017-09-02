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
from googletrans import Translator

class DairyqueencnSpider(scrapy.Spider):
		translator = Translator()
		name = "dairyqueencn"
		uid_list = []
		start_urls = ['http://www.dairyqueen.com.cn/store/']
		count = 0
		headers = {
		    "Accept":"application/json, text/javascript, */*; q=0.01",
		    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
		    "X-Requested-With":"XMLHttpRequest"
		}

		def parse(self, response):
			regions = response.xpath('//ul[@id="storemove"]//a')
			for region in regions:
				region_id = region.xpath('./@id').extract_first()
				url = "http://www.dairyqueen.com.cn/ajax.php?action=getstorecity"
				form_data = {
				    "pid":region_id,
				}
				yield FormRequest(url=url, formdata=form_data, headers=self.headers, callback=self.parse_region)
		def parse_region(self, response):
			cities = response.xpath('//a')
			for city in cities:
				city_id = city.xpath('./@id').extract_first()[1:]
				url = "http://www.dairyqueen.com.cn/ajax.php?action=getstoreinfo"
				form_data = {
					"cid": city_id,
					"type": city.xpath('./@id').extract_first()[0]
				}
				yield FormRequest(url=url, formdata=form_data, headers=self.headers, callback=self.parse_city)
		def parse_city(self, response):
			if len(response.xpath("//div[@class='p_bar']")) != 0:
				pages_count = len(response.xpath("//div[@class='p_bar']/a")) - 1
				request_body = response.request.body.split('&')
				request_type = request_body[0].split('=')[-1]
				cid = request_body[1].split('=')[-1]
				for page in range(1, pages_count + 1):
					url = "http://www.dairyqueen.com.cn/ajax.php?action=getstoreinfo"
					form_data = {
						"cid": cid,
						"type": request_type,
						"page": str(page)
					}
					yield FormRequest(url=url, formdata=form_data, headers=self.headers, callback=self.parse_store)
			else:
				self.parse_store(response)
		def parse_store(self, response):		    	
			stores = response.xpath('//table[1]/tr')
			for store in stores:
				item = ChainItem()
				item['store_number'] = ""
				item['store_name'] = self.translator.translate(self.validate(store.xpath('.//td[@class="STYLE1"][1]/text()').extract_first())).text
				item['address'] = self.translator.translate(self.validate(store.xpath('.//td[@class="STYLE1"][2]/text()').extract_first())).text
				item['address2'] = ""
				item['city'] = ""
				item['state'] = ""
				item['zip_code'] = ""
				item['country'] = "China"
				item['phone_number'] = ""
				item['store_hours'] = ""			
				item['latitude'] = ""
				item['longitude'] = ""
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
