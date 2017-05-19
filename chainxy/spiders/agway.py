import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class AgwaySpider(scrapy.Spider):
	name = "agway"
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
			request_url = "http://www.agway.com/StoreLocations/results.aspx?long=" + str(info['longitude']) + "&lat=" + str(info['latitude']) + "&zip=&address=&city=" + info['city'].replace(' ', '+') + "&state=" + self.us_state_abbrev[info['state']] + "&Num=10&SearchAddress=" + info['city'].replace(' ', '+') + "%2c+" + self.us_state_abbrev[info['state']] + "+"
			# request_url = "http://www.agway.com/StoreLocations/results.aspx?long=-74.0059413&lat=40.7127837&zip=&address=&city=New+York&state=NY&Num=3&SearchAddress=New+York%2c+NY+"
			yield scrapy.Request(url=request_url, callback=self.parse_store)

	def parse_store(self, response):
		try:
			for store in response.xpath('//div[@id="resultslist"]/div'):
				item = ChainItem()
				item['store_name'] = self.validate(store.xpath('.//td[@class="StoreName"]/span/text()'))
				item['store_number'] = ""
				item['address'] = self.validate(store.xpath('.//span[@itemprop="street-address"]/text()'))
				item['address2'] = ""
				item['city'] = self.validate(store.xpath('.//span[@itemprop="locality"]/text()'))
				item['state'] = self.validate(store.xpath('.//span[@itemprop="region"]/text()'))
				item['zip_code'] = self.validate(store.xpath('.//span[@itemprop="postal-code"]/text()'))
				item['country'] = self.validate(store.xpath('.//span[@itemprop="country-name"]/text()'))
				item['phone_number'] = self.validate(store.xpath('//span[contains(@id, "StoreInfo_Phone")]/text()'))
				hours = store.xpath('.//div[@class="StoreHours"]//text()').extract()
				hours = [a.strip() for a in hours if a.strip() != ""]
				item['store_hours'] = ""
				for hour in hours:
					if hours.index(hour) % 2 == 0:
						item['store_hours'] += hour
					else:
						item['store_hours'] += hour + ";"
				lat_lng = self.validate(store.xpath('.//a[@class="MapThisStore"]/@onclick'))
				item['latitude'] = lat_lng.split("('")[1].split("'")[0]
				item['longitude'] = lat_lng.split("('")[1].split(",'")[1].split("')")[0]
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