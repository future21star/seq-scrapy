import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb
import yaml

class LoftSpider(scrapy.Spider):
	name = "loft"
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
	uid_list = []

	def __init__(self):
		place_file = open('cities_us.json', 'rb')
		self.place_reader = json.load(place_file)
		
	def start_requests(self):
		for info in self.place_reader:
			request_url = "https://annstorelocator.appspot.com/stores?callback=jQuery11010161914695897051_1496680397933&limit=10000&lng=%s&lat=%s&Company=ATL" % (info['longitude'], info['latitude'])
			yield scrapy.Request(url=request_url, callback=self.parse_store)

	def parse_store(self, response):
		try:
			stores = json.loads(response.body.replace('// API callback\njQuery11010161914695897051_1496680397933(', '').replace(');\n', ''))['features']
			for store in stores:
				item = ChainItem()
				item['store_name'] = store['properties']['Store_Name']
				item['store_number'] = store['properties']['Store_Id']
				item['address'] = store['properties']['Store_Address1']
				item['address2'] = ""
				item['city'] = store['properties']['Store_City']
				item['state'] = store['properties']['Store_State']
				item['zip_code'] = store['properties']['Store_Zip']
				item['country'] = store['properties']['Country_Id']
				item['phone_number'] = store['properties']['Store_Phone']
				item['store_hours'] = store['properties']['Store_Hours'].replace('<br/>', ';')
				item['latitude'] = store['geometry']['coordinates'][1]
				item['longitude'] = store['geometry']['coordinates'][0]
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = 0
				yield item
		except:
			pass

	def validate(self, xpath):
		try:
			return xpath.extract_first().strip()
		except:
			return ""