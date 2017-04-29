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

class DollartreecanadaSpider(scrapy.Spider):
		name = "dollartreecanada"
		uid_list = []
		start_urls = ['https://hosted.where2getit.com/dollartreeca/ajax?&xml_request=%3Crequest%3E%3Cappkey%3E411A7C8E-6139-11E4-96F6-36D9F48ECC77%3C%2Fappkey%3E%3Cformdata+id%3D%22locatorsearch%22%3E%3Cdataview%3Estore_default%3C%2Fdataview%3E%3Climit%3E250%3C%2Flimit%3E%3Cgeolocs%3E%3Cgeoloc%3E%3Caddressline%3Es7h%3C%2Faddressline%3E%3Clongitude%3E%3C%2Flongitude%3E%3Clatitude%3E%3C%2Flatitude%3E%3Ccountry%3E%3C%2Fcountry%3E%3C%2Fgeoloc%3E%3C%2Fgeolocs%3E%3Csearchradius%3E5000%3C%2Fsearchradius%3E%3Cradiusuom%3Ekm%3C%2Fradiusuom%3E%3Cwhere%3E%3Ccountry%3E%3Ceq%3ECA%3C%2Feq%3E%3C%2Fcountry%3E%3C%2Fwhere%3E%3C%2Fformdata%3E%3C%2Frequest%3E']
		def parse(self, response):
			try:
				for store in response.xpath('//poi'):
					item = ChainItem()
					item['store_number'] = self.validate(store.xpath('./clientkey/text()'))
					item['store_name'] = self.validate(store.xpath('./name/text()'))
					item['address'] = self.validate(store.xpath('./address1/text()'))
					item['address2'] = self.validate(store.xpath('./address2/text()'))
					item['city'] = self.validate(store.xpath('./city/text()'))
					item['state'] = self.validate(store.xpath('./province/text()'))
					item['zip_code'] = self.validate(store.xpath('./postalcode/text()'))
					item['country'] = "Canada" 
					item['phone_number'] = self.validate(store.xpath('./phone/text()'))
					item['latitude'] = self.validate(store.xpath('./latitude/text()'))
					item['longitude'] = self.validate(store.xpath('./longitude/text()'))
					item['store_hours'] = self.validate(store.xpath('./monhours/text()')) + ";" + self.validate(store.xpath('./monhours/text()')) + ";" + self.validate(store.xpath('./tuehours/text()')) + ";" + self.validate(store.xpath('./wedhours/text()')) + ";" + self.validate(store.xpath('./thuhours/text()')) + ";" + self.validate(store.xpath('./frihours/text()')) + ";" + self.validate(store.xpath('./sathours/text()')) + ";" + self.validate(store.xpath('./sunhours/text()')) + ";"
					#item['store_type'] = info_json["@type"]
					item['other_fields'] = ""
					item['coming_soon'] = 0
					yield item
			except:
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