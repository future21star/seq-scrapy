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

class ClubfitnessSpider(scrapy.Spider):
    name = "clubfitness"
    uid_list = []
    start_urls = ['http://www.clubfitness.us/locations/']

    def parse(self, response):
        stores = response.xpath('//li[contains(@class, "corePrettyStyle prettylink map")]')
        for store in stores:
            item = ChainItem()
            location = store.xpath('.//div[@class="location"]/text()').extract()
            pdb.set_trace()
            item['store_number'] = ""
            item['store_name'] = store.xpath('./name/text()')[0][:-3]
            description = store.xpath('./description//text()')
            description = [a.strip() for a in description if a.strip() != ""]
            if self.isEndWithZipCode(description[3]):
                item['address'] = description[2]
                i = 0
            else:
                item['address'] = description[2] + " " + description[3]
                i = 1
            item['address2'] = ""
            item['city'] = description[3 + i].strip().split(',')[0].strip()
            try:
                item['state'] = description[3 + i].strip().split(',')[1].strip().split()[0].strip()
            except:
                pdb.set_trace()

            item['zip_code'] = " ".join(description[3 + i].strip().split(',')[1].strip().split()[1:]).strip()
            try: 
                zip = int(item['zip_code'])
                item['country'] = "United States" 
            except:
                item['country'] = "Canada"
            item['phone_number'] = description[5 + i].strip()
            item['store_hours'] = ""
            item['latitude'] = store.xpath('.//point/coordinates/text()')[0].split(',')[1].strip()
            item['longitude'] = store.xpath('.//point/coordinates/text()')[0].split(',')[0].strip()
            #item['store_type'] = info_json["@type"]
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




