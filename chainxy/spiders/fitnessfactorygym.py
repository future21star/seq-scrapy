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

class FitnessFactoryGymSpider(scrapy.Spider):
    name = "fitnessfactorygym"
    uid_list = []
    start_urls = ['http://www.fitnessfactorygym.com/rockaway/']
    domain = "http://www.fitnessfactorygym.com/"

    def parse(self, response):
        stores = response.xpath('//li[@id="menu-item-2323"]/ul/li/a/@href').extract()
        for store in stores:
            yield scrapy.Request(url=store, callback=self.parse_store)

    def parse_store(self, response):
        try:
            item = ChainItem()
            item['store_number'] = ""
            item['store_name'] = self.validate(response.xpath('//span[@itemprop="jobTitle"]/strong/text()'))
            addr = self.validate(response.xpath('.//article/h5/text()')).split(',')
            item['address'] = self.validate(response.xpath('//span[@itemprop="streetAddress"]/text()'))
            item['address2'] = ""
            item['city'] = self.validate(response.xpath('//span[@itemprop="addressLocality"]/text()'))
            item['state'] = self.validate(response.xpath('//span[@itemprop="addressRegion"]/text()'))
            item['zip_code'] = self.validate(response.xpath('//span[@itemprop="postalCode"]/text()'))
            item['country'] = "United States"
            item['phone_number'] = self.validate(response.xpath('//span[@class="deskcta"]/text()'))
            hours = response.xpath('//div[@class="col-sm-6 hours-map"]/p[2]/text()').extract()
            hours = [a.strip() for a in hours if a.strip() != ""]
            item['store_hours'] = ";".join(hours).encode('utf8').replace('\xe2\x80\x93', '-')
            item['latitude'] = response.body.split("lat=")[1].split('&')[0]
            item['longitude'] = response.body.split("long=")[1].split('&')[0]
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




