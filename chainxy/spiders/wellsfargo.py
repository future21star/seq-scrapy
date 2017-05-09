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

class WellsfargoSpider(scrapy.Spider):
    name = "wellsfargo"
    uid_list = []
    start_urls = ['https://www.wellsfargo.com/locator/']
    domain = "https://www.wellsfargo.com/locator/as/getCities/"

    def parse(self, response):
    		states = response.xpath('//map[@name="theImageMap"]/area')
    		for state in states:
    			state_value = state.xpath('./@href').extract_first()[1:]
    			request = scrapy.Request(url = self.domain + state_value, callback=self.parse_city)
    			item = ChainItem()
    			item['state'] = state_value
    			request.meta['item'] = item
    			yield request

    def parse_city(self, response):
    	try:
				item = response.meta['item']
				cities = json.loads(response.body[35: -25])["allCities"]
				for city in cities:
					item['city'] = city
					url = "https://www.wellsfargo.com/locator/search/?searchTxt=" + city.replace(" ", "+") + "%2C+" + item['state'] + "&mlflg=N&sgindex=99&chflg=Y&il=EN&_bo=on&_wl=on&_os=on&_bdu=on&_adu=on&_ah=on&_sdb=on&_aa=on&_nt=on&_fe=on&_ss=on"
					request = scrapy.Request(url = url, callback=self.parse_store)
					request.meta['item'] = item
					yield request
    	except:
    		pass
    def parse_store(self, response):
		item = response.meta['item']
		stores = response.xpath('//li[@class="aResult"]')
		for store in stores:
				item = ChainItem()
				item['store_number'] = ""
				item['store_name'] = self.validate(store.xpath('.//address/div[@class="fn heading"]/text()'))
				item['address'] = self.validate(store.xpath('.//address/div[@class="street-address"]/text()'))
				item['address2'] = ""
				item['city'] = self.validate(store.xpath('.//span[@class="locality"]/text()'))
				item['state'] = self.validate(store.xpath('.//abbr[@class="region"]/text()'))
				item['zip_code'] = self.validate(store.xpath('.//span[@class="postal-code"]/text()'))
				item['country'] = "United States" 
				item['phone_number'] = self.validate(store.xpath('.//div[@class="tel"]/text()')).split(':')[-1].strip()
				item['store_hours'] = ""
				if (self.validate(store.xpath('.//div[@class="rightSideData"]/div[@class="heading"]/text()')) == "Lobby Hours"):
						hours = store.xpath('.//div[@class="rightSideData"]/ul[@lang="en"]//text()').extract()
						hours = [a.strip() for a in hours if a.strip() != ""]
						item['store_hours'] = ";".join(hours)
				item['latitude'] = self.validate(store.xpath('./@data-location')).split(',')[0]
				item['longitude'] = self.validate(store.xpath('./@data-location')).split(',')[1]
				#item['store_type'] = info_json["@type"]
                if item['phone_number'] != "" and item['phone_number'] in self.uid_list:
                    continue
                self.uid_list.append(item['phone_number'])
				item['other_fields'] = ""
				item['coming_soon'] = 0
				yield item
        # except:
            # pass            

    def validate(self, xpath):
        try:
            return self.replaceUnknownLetter(xpath.extract_first().strip())
        except:
            return ""

    def isEndWithZipCode(self, str):
        str = str[-5:]
        count = 0
        if str[0].isdigit():
            for char in str:
                if char.isdigit():
                    count += 1
            if count == 5:
                return True
        str = str[-3:]
        if (str[0].isdigit() and (not str[1].isdigit()) and str[2].isdigit()):
            return True            
        return False

    def replaceUnknownLetter(self, source):
        try:
            formatted_value = source.encode('utf8').replace('\xc3', '').replace('\xa9', 'e').replace('\xa8', 'e').replace('\xb4', 'o').replace('\xb3', 'o').replace('\xb9', 'u').replace('\xba', 'u').replace('\x89', 'E').replace('\xaa', 'e').replace('\x89', 'E').replace('\xa2', 'a').replace('\xac', 'i').replace('\xad', 'i').replace('\xae', 'i')
            # if "x8" in formatted_value or "x9" in formatted_value or "xa" in formatted_value or "xb" in formatted_value:
            #   pdb.set_trace()
            return formatted_value
        except:
            return source
    def format(self, item):
        try:
            return unicodedata.normalize('NFKD', item).encode('ascii','ignore').strip()
        except:
            return ''           




