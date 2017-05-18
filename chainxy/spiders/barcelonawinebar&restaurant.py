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

class BarcelonawinebarandrestaurantSpider(scrapy.Spider):
    name = "barcelonawinebarandrestaurant"
    uid_list = []
    start_urls = ['http://www.barcelonawinebar.com/locations/']
    domain = 'https://www.bgrtheburgerjoint.com'

    def parse(self, response):
        try:
            stores = response.xpath('//ul[@class="loc clearfix"]//a[contains(@href, "http://www.barcelonawinebar.com/location/")]/@href').extract()
            for store in stores:
                yield scrapy.Request(url=store, callback=self.parse_store)
        except:
            pdb.set_trace()
            pass
    def parse_store(self, response):
        try:
            item = ChainItem()
            store = response 
            item['store_number'] = ""
            item['store_name'] = self.validate(store.xpath('//div[@class="location"]/h1/text()'))
            addr = store.xpath('//div[@class="td-inner"]/address[1]/text()').extract()
            item['address2'] = ""
            try:
                item['address'] = addr[0].strip()
                item['city'] = addr[1].split(',')[0].strip()
                item['state'] = addr[1].split(',')[1].split()[0].strip()
                item['zip_code'] = addr[1].split(',')[1].split()[1].strip()
            except:
                item['address'] = addr[0].split(',')[0]
                item['city'] = addr[0].split(',')[1]
                item['state'] = "CA"
                item['zip_code'] = ""
            item['country'] = "United States"
            item['phone_number'] = store.xpath('//a[contains(@href, "tel:")]/@href').extract_first().split(":")[-1].replace('.', '-').strip()
            hours = store.xpath('//div[@class="td-inner"]/time/p[1]//text()').extract()
            hours = [a.strip() for a in hours if a.strip() != ""]
            item['store_hours'] = ""
            for hour in hours:
                if hours.index(hour) % 2 == 0:
                    item['store_hours'] += hour + ":"
                else:
                    item['store_hours'] += hour + ";"
            lat_lng = store.xpath('//a[contains(@href, "https://www.google.com/maps/search/")]/@href').extract_first()
            item['latitude'] = lat_lng.split("@")[-1].split(',')[0]
            item['longitude'] = lat_lng.split("@")[-1].split(',')[1]
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




