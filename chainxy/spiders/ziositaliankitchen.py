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

class ZiositaliankitchenSpider(scrapy.Spider):
    name = "ziositaliankitchen"
    uid_list = []
    start_urls = ['https://zios.com/locations/?disp=all']

    def parse(self, response):
        try:
            stores = response.xpath('//div[@class="panel panel-default"]//ul/li/div')
            for store in stores:
                item = ChainItem()
                item['store_number'] = store.xpath('./p[4]/a/@href').extract_first().split("=")[-1].strip()
                item['store_name'] = self.validate(store.xpath('.//h4/text()'))
                addr = store.xpath('./p[1]/text()').extract()
                item['address'] = addr[0].strip()
                item['address2'] = ""
                item['city'] = addr[1].split(',')[0].strip()
                item['zip_code'] = addr[1].split(',')[1].split()[1]
                item['state'] = addr[1].split(',')[1].split()[0]
                item['country'] = "United States"
                item['phone_number'] = addr[2].split(":")[-1].strip()
                hours = store.xpath('./p[2]/text()').extract()
                hours = [a.strip() for a in hours if a.strip() != ""]
                item['store_hours'] = ";".join(hours)
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




