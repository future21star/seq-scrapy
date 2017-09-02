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

class GuesthouseintlSpider(scrapy.Spider):
		translator = Translator()
		name = "guesthouseintl"
		uid_list = []
		start_urls = ['https://www.redlion.com/guesthouse']
		count = 0

		def parse(self, response):
			pdb.set_trace()
			states = json.loads(response.body.split("var brandMapJSON = ")[-1].split("; </script>")[0])['United States']['states']
			for state in states:
				state_abbr = states[state]["state_abbr"]
				url = "https://www.redlion.com/search/results?type=region&id=US-" + state_abbr + "&lang=en&sort=name&brands%5B0%5D=4&page=1&perpage=10"
				yield scrapy.Request(url=url, callback=self.parse_state)

		def parse_state(self, response):
											
			for store in response.body.split("google.maps.event.addListener")[1:]:
				item = ChainItem()
				if store.find("$('.mapPopInfo li').find('strong').html('") == -1:
					continue
				item['store_number'] = ""
				item['store_name'] = self.translator.translate(store.split("$('.mapPopInfo li').find('strong').html('")[-1].split("');")[0]).text
				item['address'] = self.translator.translate(store.split("$('.mapPopInfo li').eq(1).html('")[-1].split("');")[0]).text
				item['address2'] = ""
				item['city'] = ""
				item['state'] = ""
				item['zip_code'] = ""
				item['country'] = "China"
				item['phone_number'] = self.translator.translate(store.split("$('.mapPopInfo li').eq(2).html('")[-1].split("');")[0]).text
				item['store_hours'] = ""
				if store.find("\xe6\xaf\x8f\xe5\xa4\xa9:") != -1:
					item['store_hours'] = store.split("\xe6\xaf\x8f\xe5\xa4\xa9:")[-1].split("');")[0]
				elif store.find("Everyday:") != -1:
					item['store_hours'] = store.split("Everyday:")[-1].split("');")[0]
				elif store.find("Everyday\xef\xbc\x9a") != -1:
					item['store_hours'] = store.split("Everyday\xef\xbc\x9a")[-1].split("');")[0]
				elif store.find("\xe6\xaf\x8f\xe5\xa4\xa9\xef\xbc\x9a") != -1:
					item['store_hours'] =  store.split("\xe6\xaf\x8f\xe5\xa4\xa9\xef\xbc\x9a")[-1].split("');")[0]
				elif store.find("\xe6\x97\xa5\xef\xbc\x9a") != -1:
					item['store_hours'] =  store.split("\xe6\x97\xa5\xef\xbc\x9a")[-1].split("');")[0]
				elif store.find("\xe6\xaf\x8f\xe5\xa4\xa9") != -1:
					item['store_hours'] =  store.split("\xe6\xaf\x8f\xe5\xa4\xa9")[-1].split("');")[0]				
				elif store.find("\xe5\x85\xad\xef\xbc\x9a") != -1:
					item['store_hours'] =  store.split("\xe5\x85\xad\xef\xbc\x9a")[-1].split("');")[0]		
				elif store.find("\xe5\x85\xad\xef\xbc\x9a:") != -1:
					item['store_hours'] =  store.split("\xe5\x85\xad\xef\xbc\x9a:")[-1].split("');")[0]						
				elif store.find("\xe5\x91\xa8\xe5\x85\xad") != -1:
					item['store_hours'] =  store.split("\xe5\x91\xa8\xe5\x85\xad")[-1].split("');")[0]									
				elif store.find("\xe5\x91\xa8\xe5\x85\xad: ") != -1:
					item['store_hours'] =  store.split("\xe5\x91\xa8\xe5\x85\xad: ")[-1].split("');")[0]									
				elif store.find("\xe5\x91\xa8\xe5\x85\xad") != -1:
					item['store_hours'] =  store.split("\xe5\x91\xa8\xe5\x85\xad")[-1].split("');")[0]									
				elif store.find("\xe5\x91\xa8\xe6\x97\xa5") != -1:
					item['store_hours'] =  store.split("\xe5\x91\xa8\xe6\x97\xa5")[-1].split("');")[0]									
				elif store.find("\xe5\x91\xa8\xe6\x97\xa5 ") != -1:
					item['store_hours'] =  store.split("\xe5\x91\xa8\xe6\x97\xa5 ")[-1].split("');")[0]									
				elif store.find("\xe5\x91\xa8\xe6\x97\xa5: ") != -1:
					item['store_hours'] =  store.split("\xe5\x91\xa8\xe6\x97\xa5: ")[-1].split("');")[0]									
				elif store.find("\xe6\x97\xb6\xef\xbc\x9a") != -1:
					item['store_hours'] =  store.split("\xe6\x97\xb6\xef\xbc\x9a")[-1].split("');")[0]						
				elif store.find("\xe6\x9c\x9f\xe5\x85\xad:") != -1:
					item['store_hours'] =  store.split("\xe6\x9c\x9f\xe5\x85\xad:")[-1].split("');")[0]	
				if store.find("\xe5\x88\x9d\xe4\xb8\x89") != -1:
					item['store_hours'] =  store.split("\xe5\x88\x9d\xe4\xb8\x89")[-1].split("');")[0]
				item['store_hours'] = item['store_hours'].replace("\xe2\x80\x93", '-')
				item['latitude'] = store.split("new google.maps.LatLng(")[-1].split('),')[0].split(',')[0]
				item['longitude'] = "-" + store.split("new google.maps.LatLng(")[-1].split('),')[0].split(',')[1]
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
