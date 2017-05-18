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
class BornshoesSpider(scrapy.Spider):
		name = "bornshoes"
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
			place_file = open('cities_us.json', 'rb')
			self.place_reader = json.load(place_file)

		def start_requests(self):
			for info in self.place_reader:
				city = info['city'].replace(" ", "%20")
				url = "http://locator.hhbrown.com/Soa/4.0/HHBrownStores4.svc/GetStoresByBrand?b=04SH&z=%s,%s&d=100&callback=jQuery22406102562250571344_1495080415265&_=1495080415332" % (city, self.us_state_abbrev[info['state']])
				yield scrapy.Request(url=url, callback=self.parse)
			
		def parse(self, response):
			try:
				pdb.set_trace()
				stores = yaml.load(response	.body.split("jQuery22406102562250571344_1495080415265(")[-1].split(");")[0])['Locations']
				for store in stores:
					item = ChainItem()
					item['store_number'] = store['Locator_Store_ID']
					item['store_name'] = store['Name']
					item['address'] = store['Address1']
					item['address2'] = store['Address2']
					addr = store['CityStateZip']
					item['city'] = store['City']
					item['state'] = store['State']
					item['zip_code'] = store['Zip']
					item['country'] = "United States" 
					item['phone_number'] = store['Phone']
					item['store_hours'] = ""
					item['latitude'] = store['G_Latitude']
					item['longitude'] = store['G_Longitude']
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




