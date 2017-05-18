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

class BgrtheburgerjointburgerjointSpider(scrapy.Spider):
    name = "bgrtheburgerjointburgerjoint"
    uid_list = []
    start_urls = ['https://www.bgrtheburgerjoint.com/locations-menus/']
    domain = 'https://www.bgrtheburgerjoint.com'

    def parse(self, response):
        stores = response.xpath('//div[@class="x-accordion-inner"]/a/@href').extract()
        for store in stores:
            url = self.domain + store.replace('locations', 'locations-menus')
            yield scrapy.Request(url=url, callback=self.parse_store)

    def parse_store(self, response):
        try:
            store = response
            item = ChainItem()
            item['store_number'] = ""
            item['store_name'] = self.validate(store.xpath('//div[@class="x-column x-sm x-2-5"]/h1/span/text()'))
            addr = store.xpath('//div[@class="x-column x-sm cs-ta-center man x-1-2"]/div[@class="x-text"][1]//text()').extract()
            item['address'] = addr[1].strip()
            item['address2'] = ""
            item['city'] = addr[2].split(',')[0].strip()
            item['state'] = addr[2].split(',')[1].split()[0]
            item['zip_code'] = addr[2].split(',')[1].split()[1]
            item['country'] = "United States"
            item['phone_number'] = store.xpath('//a[contains(@href, "tel:")]/@href').extract_first().split(":")[-1]
            hours = store.xpath('//div[@class="x-column x-sm cs-ta-center man x-1-2"]/div[@class="x-text"][2]//text()').extract()
            hours = [a.strip() for a in hours if a.strip() != ""][1:]
            item['store_hours'] = ";".join(hours)
            lat_lng = store.xpath('//div[@class="x-map x-google-map man"]/@data-x-params').extract_first()
            item['latitude'] = lat_lng.split(",")[0].split('"')[-2]
            item['longitude'] = lat_lng.split(",")[1].split('"')[-2]
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




