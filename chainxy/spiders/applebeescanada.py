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

class ApplebeescanadaSpider(scrapy.Spider):
    name = "applebeescanada"
    uid_list = []
    start_urls = ['http://www.applebeescanada.com/']
    domain = "http://www.applebeescanada.com"

    def parse(self, response):
        states = response.xpath('//div[@class="scroll-pane"]/ul/li')
        for state in states:
            item = ChainItem()
            item['state'] = self.validate(state.xpath('./a/text()'))
            stores = state.xpath('./ul//a')   
            for store in stores:
                url = self.domain + store.xpath('./@href').extract_first()
                request = scrapy.Request(url=url, callback=self.parse_store)
                request.meta['item'] = item
                yield request

    def parse_store(self, response):
        try:
            item = response.meta['item']
            store = response.xpath('//div[@class="blocks"]')
            item['store_number'] = ""
            item['store_name'] = self.validate(store.xpath('.//h1/text()'))
            item['address2'] = ""
            try:
                addr = self.validate(store.xpath('.//article/h5/text()')).split(',')
                item['address'] = addr[1].strip()
                item['city'] = addr[0].strip()
                item['zip_code'] = addr[2].strip()
            except:
                addr = store.xpath('.//article/h5/text()').extract()
                item['address'] = addr[0].strip()[:-1].strip()
                item['city'] = addr[1].split(',')[0].strip()
                item['zip_code'] = " ".join(addr[1].split(',')[1].split()[1:]).strip()
            item['zip_code'] = item['zip_code'].replace('Unit 240', '')
            if item['zip_code'] == 'Calgary':
                item['zip_code'] = addr[-1].strip()
            item['country'] = "Canada"
            item['phone_number'] = self.validate(store.xpath('.//article/h3[@class="txtrojo"]/text()')).replace('Call', '').strip()
            hours = store.xpath('.//article/p[1]//text()').extract()
            hours = [a.strip() for a in hours if a.strip() != ""]
            item['store_hours'] = ""
            for hour in hours:
                if hours.index(hour) % 2 == 0:
                    item['store_hours'] += hour + ":"
                else:
                    item['store_hours'] += hour + ";"
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

class ApplebeescanadaSpider(scrapy.Spider):
    name = "applebeescanada"
    uid_list = []
    start_urls = ['http://www.applebeescanada.com/']
    domain = "http://www.applebeescanada.com"

    def parse(self, response):
        states = response.xpath('//div[@class="scroll-pane"]/ul/li')
        for state in states:
            item = ChainItem()
            item['state'] = self.validate(state.xpath('./a/text()'))
            stores = state.xpath('./ul//a')   
            for store in stores:
                url = self.domain + store.xpath('./@href').extract_first()
                request = scrapy.Request(url=url, callback=self.parse_store)
                request.meta['item'] = item
                yield request

    def parse_store(self, response):
        try:
            item = response.meta['item']
            store = response.xpath('//div[@class="blocks"]')
            item['store_number'] = ""
            item['store_name'] = self.validate(store.xpath('.//h1/text()'))
            item['address2'] = ""
            try:
                addr = self.validate(store.xpath('.//article/h5/text()')).split(',')
                item['address'] = addr[1].strip()
                item['city'] = addr[0].strip()
                item['zip_code'] = addr[2].strip()
            except:
                addr = store.xpath('.//article/h5/text()').extract()
                item['address'] = addr[0].strip()[:-1].strip()
                item['city'] = addr[1].split(',')[0].strip()
                item['zip_code'] = " ".join(addr[1].split(',')[1].split()[1:]).strip()
            item['zip_code'] = item['zip_code'].replace('Unit 240', '')
            if item['zip_code'] == 'Calgary':
                item['zip_code'] = addr[-1].strip()
            item['country'] = "Canada"
            item['phone_number'] = self.validate(store.xpath('.//article/h3[@class="txtrojo"]/text()')).replace('Call', '').strip()
            hours = store.xpath('.//article/p[1]//text()').extract()
            hours = [a.strip() for a in hours if a.strip() != ""]
            item['store_hours'] = ""
            for hour in hours:
                if hours.index(hour) % 2 == 0:
                    item['store_hours'] += hour + ":"
                else:
                    item['store_hours'] += hour + ";"
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




