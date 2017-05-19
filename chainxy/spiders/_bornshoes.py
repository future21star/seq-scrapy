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
class BornshoesMakerSpider(scrapy.Spider):
		name = "_bornshoes"
		uid_list = []
		us_state_abbrev = {
		    'Alabama': 'AL',
		    'Alaska': 'AK',
		    'Arizona': 'AZ',
		    'Arkansas': 'AR',
		    'California': 'CA',
		    'Colorado': 'CO',
		    'Connecticut': 'CT',
		    'Delaware': 'DE',
		    'Florida': 'FL',
		    'Georgia': 'GA',
		    'Hawaii': 'HI',
		    'Idaho': 'ID',
		    'Illinois': 'IL',
		    'Indiana': 'IN',
		    'Iowa': 'IA',
		    'Kansas': 'KS',
		    'Kentucky': 'KY',
		    'Louisiana': 'LA',
		    'Maine': 'ME',
		    'Maryland': 'MD',
		    'Massachusetts': 'MA',
		    'Michigan': 'MI',
		    'Minnesota': 'MN',
		    'Mississippi': 'MS',
		    'Missouri': 'MO',
		    'Montana': 'MT',
		    'Nebraska': 'NE',
		    'Nevada': 'NV',
		    'New Hampshire': 'NH',
		    'New Jersey': 'NJ',
		    'New Mexico': 'NM',
		    'New York': 'NY',
		    'North Carolina': 'NC',
		    'North Dakota': 'ND',
		    'Ohio': 'OH',
		    'Oklahoma': 'OK',
		    'Oregon': 'OR',
		    'Pennsylvania': 'PA',
		    'Rhode Island': 'RI',
		    'South Carolina': 'SC',
		    'South Dakota': 'SD',
		    'Tennessee': 'TN',
		    'Texas': 'TX',
		    'Utah': 'UT',
		    'Vermont': 'VT',
		    'Virginia': 'VA',
		    'Washington': 'WA',
		    'West Virginia': 'WV',
		    'Wisconsin': 'WI',
		    'Wyoming': 'WY',
		    'District of Columbia': 'DC'
		}
		start_urls = ["https://www.bornshoes.com"]
		def __init__(self):
			place_file = open('_bornshoes_20170517.csv', 'rb')
			self.place_reader = csv.reader(place_file)
			
		def parse(self, response):
			try:
				for store in self.place_reader:
					if store[0] != "store_name":
						try:
							item = ChainItem()
							item['store_number'] = store[1]
							item['store_name'] = store[0]
							if store[3] != "" and store[3][0].isdigit():
								item['address'] = store[3]
								item['address2'] = store[2]
							else:
								item['address'] = store[2]
								item['address2'] = store[3]						
							item['city'] = store[4]
							item['state'] = store[5]
							item['zip_code'] = store[6]
							item['country'] = store[7]
							item['phone_number'] = store[8]
							item['store_hours'] = store[11]
							item['latitude'] = store[9]
							item['longitude'] = store[10]
							#item['store_type'] = info_json["@type"]
							item['other_fields'] = ""
							item['coming_soon'] = 0
							yield item
						except:
							pdb.set_trace()
							pass
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




