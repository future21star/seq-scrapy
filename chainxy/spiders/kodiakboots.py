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

class KodiakbootsSpider(scrapy.Spider):
		translator = Translator()
		name = "kodiakboots"
		uid_list = []
		count = 0
		headers = {
		    "Accept":"application/json, text/javascript, */*; q=0.01",
		    "Content-Type":"application/json;charset=UTF-8",
		    "X-Requested-With":"XMLHttpRequest"
		}
		states_list = []

		def __init__(self):
			place_file = open('citiesusca.json', 'rb')
			self.place_reader = json.load(place_file)

		def start_requests(self):
			for key in self.place_reader:
				info = self.place_reader[key]
				if info["country"] == "Canada":
					# if info["state"] in self.states_list:
					# 	continue
					self.states_list.append(info['state'])
					url = "http://hosted.where2getit.com/kodiakfootwear/rest/locatorsearch?like=0.08600414372186571&lang=en_US"
					form_data = {"request":{"appkey":"1956A226-4397-11E6-AA8B-99F9A38844B8","formdata":{"geoip":'false',"dataview":"store_default","limit":250,"geolocs":{"geoloc":[{"addressline":info["city"].split("(")[0],"country":"CA","latitude":"","longitude":""}]},"searchradius":"15|25|50|100|250","where":{"or":{"MENS_SAFETY":{"eq":""},"WOMENS_SAFETY":{"eq":""},"MENS_CLASSIC":{"eq":""},"MENS_WINTER":{"eq":""},"WOMENS_CLASSIC":{"eq":""},"WOMENS_WINTER":{"eq":""},"KIDS":{"eq":""}}},"'false'":"0"}}}
					yield FormRequest(url=url, body=json.dumps(form_data), headers=self.headers, callback=self.parse_city)

		def parse_city(self, response):		    	
			if 'collection' in json.loads(response.body)['response']:
				stores = json.loads(response.body)['response']['collection']
				for store in stores:
					item = ChainItem()
					item['store_number'] = self.getVal(store, "uid")
					item['store_name'] = self.getVal(store, "name")
					item['address'] = self.getVal(store, "address1")
					item['address2'] = ""
					if self.getVal(store, 'address2') != None:
						item['address2'] = self.getVal(store, 'address2')
					item['city'] = self.getVal(store, "city")
					item['state'] = self.getVal(store, "province")
					item['zip_code'] = self.getVal(store, "postalcode")
					item['country'] = self.getVal(store, "country")
					item['phone_number'] = self.getVal(store, "phone")
					days = ["mon", "tues", "wed", "thurs", "fri", "sat", "sun"]
					item['store_hours'] = ""
					for day in days:
						if self.getVal(store, day+"_open") != "" and self.getVal(store, day+"_open") != None:
							item['store_hours'] += day + "day:" + self.getVal(store, day+"_open") + " - "
						if self.getVal(store, day+"_close") != "" and self.getVal(store, day+"_close") != None:
							item['store_hours'] += self.getVal(store, day+"_close") + ";"
					item['latitude'] = self.getVal(store, "latitude")
					item['longitude'] = self.getVal(store, "longitude")
					#item['store_type'] = info_json["@type")
					item['other_fields'] = ""
					item['coming_soon'] = 0
					if item['store_number'] != "" and item['store_number'] in self.uid_list:
						continue
					self.uid_list.append(item['store_number'])
					yield item

		def getVal(self, src, attr):
			if attr in src:
				return src[attr]
			return ""
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
