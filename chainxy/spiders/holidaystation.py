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

class HolidaystationSpider(scrapy.Spider):
    name = "holidaystation"
    uid_list = []
    start_urls = ['http://www.holidaystationstores.com/Locations/search']

    def parse(self, response):
        stores = yaml.load((response.body.split("var Data =")[-1].split('};')[0] + '}').strip())
        for store in stores:
            url = "http://www.holidaystationstores.com/Locations/store/" + store
            item = ChainItem()
            item['store_number'] = store
            item['latitude'] = stores[store]['Lat']
            item['longitude'] = stores[store]['Lng']
            request = scrapy.Request(url=url, callback=self.parse_store)
            request.meta['item'] = item
            yield request

    def parse_store(self, response):
        try:
            item = response.meta['item']
            detail = response.xpath('//div[@id="StoreDetails"]/div[1]/text()').extract()
            item['store_name'] = ""
            item['address'] = detail[1].strip()
            item['address2'] = ""
            item['city'] = detail[2].split(',')[0].strip()
            item['state'] = detail[2].split(',')[1].strip()
            item['zip_code'] = detail[2].split(',')[2].strip()
            item['country'] = "United States"
            item['phone_number'] = response.xpath('//div[@id="StoreDetails"]/div[1]/div[1]/a/text()').extract_first().replace('None', '')
            item['store_hours'] = ""
            try:
                item['store_hours'] = response.xpath('//div[@id="StoreDetails"]/div[1]/div[2]/span/text()').extract_first().replace('None', '')
            except:
                hours = response.xpath('//div[@id="StoreDetails"]/div[1]/div[2]/table/tr')
                for hour in hours:
                    hour_value = hour.xpath('.//text()').extract()
                    hour_value = [a.strip() for a in hour_value if a.strip() != ""]
                    item['store_hours'] += hour_value[0][:-1] + ":" + hour_value[1] + ";"
            item['other_fields'] = ""
            item['coming_soon'] = 0
            yield item
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