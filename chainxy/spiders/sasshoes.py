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
class SasshoesSpider(scrapy.Spider):
		name = "sasshoes"
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
		def __init__(self):
			place_file = open('citiesusca.json', 'rb')
			self.place_reader = json.load(place_file)

		def start_requests(self):
			for _city in self.place_reader:
				info = self.place_reader[_city]
				city = info['city'].replace(" ", "%20")
				url = "https://sasshoes.com/store-locator?q=" + info['city'].replace(' ', '+') + "%2C+" + info['state'] + "+" + info['zip_code'] + "%2C+USA&lat=" + info['latitude'] + "&lng=" + info['longitude'] + "&limit=100"
				yield scrapy.Request(url=url, callback=self.parse)
			
		def parse(self, response):
			try:
				stores = json.loads(response.body)['locations']
				for store in stores:
					item = ChainItem()
					item['store_number'] = store['store-number']
					item['store_name'] = store['store-name']
					item['store_type'] = store['store-type']
					item['address'] = store['address-1']
					item['address2'] = store['address-2']
					item['city'] = store['city']
					item['state'] = store['region']
					item['zip_code'] = store['postal-code']
					item['country'] = store['country']
					item['phone_number'] = store['phone']
					item['store_hours'] = ""
					if store['operating-hours'] != "":
						hours = json.loads(store['operating-hours'])
						days = ['mon','tue','wed', 'thu','fri','sat','sun']
						for day in days:
							item['store_hours'] += day + ":" + hours[day]["start"] + "-" + hours[day]["end"] + ";"
					item['latitude'] = store['lat']
					item['longitude'] = store['lng']
					item['other_fields'] = ""
					item['coming_soon'] = 0
					if item['store_number'] != "" and item['store_number'] in self.uid_list:
						continue
					self.uid_list.append(item['store_number'])	
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




