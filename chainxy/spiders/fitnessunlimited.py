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
import usaddress

class FitnessunlimitedSpider(scrapy.Spider):
    name = "fitnessunlimited"
    uid_list = []
    start_urls = ['https://fitnessunlimited.net/locations/']

    def parse(self, response):
        try:
            stores = json.loads(response.body.split("var gmpAllMapsInfo =")[1].split('}];')[0]+"}]")[0]['markers']
            for store in stores:
                item = ChainItem()
                item['store_number'] = store['id']
                item['store_name'] = ""
                _addr = store['address']
                addr = usaddress.parse(_addr.strip())
                item['address'] = item['address2'] = item['city'] = item['zip_code'] = item['state'] = ""
                for temp in addr:
                    if temp[1] == 'PlaceName':
                        item['city'] = temp[0].replace(',', '')
                    elif temp[1] == 'StateName':
                        item['state'] = temp[0].replace(',', '')
                    elif temp[1] == 'ZipCode':
                        item['zip_code'] = temp[0].replace(',', '')
                item['address'] = _addr.replace(',', '').replace(item['city'], '').replace(item['state'],'').replace(item['zip_code'],'').replace('USA', '').strip()
                item['country'] = "United States"
                item['phone_number'] = store['description'].split('Contact us at : ')[1].split(' ')[0]
                hours = response.xpath('//div[@class="confit-hours"]/text()').extract()
                hours = [a.strip() for a in hours if a.strip() != ""]
                item['store_hours'] = ";".join(hours[1:])
                item['latitude'] = store['coord_x']
                item['longitude'] = store['coord_y']
                #item['store_type'] = info_json["@type"]
                item['other_fields'] = ""
                item['coming_soon'] = 0
                yield item
        except:
            pdb.set_trace()
            pass
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




