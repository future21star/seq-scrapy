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
import yaml

class FogodechaoSpider(scrapy.Spider):
    name = "fogodechao"
    uid_list = []
    start_urls = ['https://fogodechao.com/locations']

    def parse(self, response):
        try:
            stores = self.getInfo(response)
            for _store in stores:
                store = _store.split(',')
                item = ChainItem()
                item['store_number'] = ""
                item['store_name'] = ""
                item['address'] = store[2][2:].strip()
                item['address2'] = ""
                item['city'] = store[0][2:].strip()
                item['state'] = store[1][7:-1].strip()
                if "." in store[4]:
                    item['zip_code'] = store[3][:-1].strip()
                    item['latitude'] = store[4].strip()
                    item['longitude'] = store[5].strip()
                else:
                    item['zip_code'] = store[4][:-1].strip()
                    item['latitude'] = store[5].strip()
                    item['longitude'] = store[6].strip()
                item['country'] = ""
                item['phone_number'] = ""
                item['store_hours'] = ""
                item['other_fields'] = ""
                item['coming_soon'] = 0
                if "location/" in store[-1]:
                    url = "https://fogodechao.com" + store[-1][1:-2].strip()
                else:
                    url = "https://fogodechao.com" + store[-2][1:-1].strip()
                request = scrapy.Request(url=url, callback=self.parse_hour)
                request.meta['item'] = item
                yield request
        except:
            pdb.set_trace()
            pass            

    def parse_hour(self, response):
        try:
            item = response.meta['item']
            item['store_hours'] = ""
            class_values = ["time holiday_hours", "time breakfast", "time lunch", "time dinner"]
            for _class_value in class_values:
                class_value = response.xpath('//div[@class="' + _class_value + '"]')
                try:
                    part_hour = class_value.xpath('.//h3/text()').extract_first().strip() + ";"
                except:
                    part_hour = ""
                for hour in class_value.xpath('.//div[@class="hours"]'):
                    value = hour.xpath('.//text()').extract()
                    try:
                        part_hour += value[0].strip() + ":" + value[1].strip() + ";"
                    except:
                        part_hour += ""
                item['store_hours'] += part_hour
                item['phone_number'] = response.xpath('//span[@class="phone"]/text()').extract_first()[1:].strip()
                if '+1' in item['phone_number']:
                    item['country'] = "Mexico"
                elif item['phone_number'].find(')') - item['phone_number'].find('(') == 3:
                    item['country'] = "Brazil"
                else:
                    item['country'] = "United States"
            yield item
        except:
            pass
    def validate(self, xpath):
        try:
            return self.replaceUnknownLetter(xpath.extract_first().strip())
        except:
            return ""

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

    def getInfo(self, response):
        body = response.body
        pos = body.find("var markerData = ") + 18
        stores = []
        store = ""
        while body[pos: pos+2] != "];":
            if body[pos] == "[":
                store = ""
            if body[pos] == "]":
                store += "]"
                stores.append(store)
            store += body[pos]
            pos += 1
        return stores

    def validatePhoneNumber(self, phone_number):
        return phone_number.strip().replace('.', '-')        