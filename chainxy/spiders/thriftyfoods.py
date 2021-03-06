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

class ThriftyfoodsSpider(scrapy.Spider):
        name = "thriftyfoods"
        uid_list = []
        start_urls = ['https://www.thriftyfoods.com/api/en/Store/get?Latitude=48.45423&Longitude=-123.359205&Skip=0&Max=30']
        count = 0

        def parse(self, response):
            try:
                stores = json.loads(response.body)['Data']
                for store in stores:
                    item = ChainItem()
                    item['store_number'] = store['Number']
                    item['store_name'] = store['Name']
                    item['address'] = store['AddressMain']['Line']
                    item['address2'] = ""
                    item['city'] = store['AddressMain']['City']
                    item['state'] = store['AddressMain']['Province']
                    item['zip_code'] = store['AddressMain']['DisplayPostalCode']
                    item['country'] = "Canada" 
                    item['phone_number'] = store['PhoneNumberHome']['Number']
                    item['store_hours'] = store['OpeningHours']
                    item['latitude'] = store['Coordinates']['Latitude']
                    item['longitude'] = store['Coordinates']['Longitude']
                    #item['store_type'] = info_json["@type"]
                    item['other_fields'] = ""
                    item['coming_soon'] = 0
                    yield item
            except:
                pdb.set_trace()
                pass            

        def validate(self, xpath):
            try:
                return xpath.extract_first().strip()
            except:
                return ""

        def isNumber(self, number):
            count = 0
            for char in number:
                if char.isdigit():
                    count += 1
            return count > 5

        def getInfo(self, response):
            try:
                start = response.body.find("location_data.push( ") + 20
                pos = response.body.find("location_data.push( ") + 20
                info = ""
                while response.body[pos] != '}':
                    if response.body[pos:pos+2] != "\'":
                        info += response.body[pos]
                    else:
                        info += "'"
                    pos += 1
                info += '}'
                return info.decode('utf8').replace("\'", "").replace('\t','').replace('\n','')
            except:
                return ""

        def getValue(self, info, property):
            try:
                pos = info.find(property + ":") + len(property) + 2
                value = ""
                while info[pos] != ",":
                    value += info[pos]
                    pos += 1
                return value
            except:
                return ""

        def getSpecificValue(self, info, property):
            try:
                pos = info.find(property) + len(property) + 3
                value = ""
                while info[pos:pos+2] != "</":
                    value += info[pos]
                    pos += 1
                return value.strip()
            except:
                return ""