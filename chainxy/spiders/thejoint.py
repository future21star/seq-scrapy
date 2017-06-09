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
import yaml

class ThejointSpider(scrapy.Spider):
        name = "thejoint"
        uid_list = []
        start_urls = ['https://www.thejoint.com/locations']

        def parse(self, response):
            try:
                for store in response.xpath("//div[contains(@class, 'clinic clinic-open clinic-')]"):                    
                    item = ChainItem()
                    item['store_number'] = ""
                    item['store_name'] = self.validate(store.xpath('.//div[@class="clinic-name"]/a/text()'))
                    addr = store.xpath('.//div[@class="clinic-address"]/text()').extract()
                    item['address'] = addr[0].strip()
                    item['address2'] = ""
                    place = addr[1]
                    if 'Suite ' in addr[1] or 'Ste ' in addr[1]:
                        item['address'] += " " + addr[1].strip()
                        place = addr[2]
                    item['city'] = place.split(',')[0].strip()
                    item['state'] = place.split(',')[1].strip().split()[0].strip()
                    item['zip_code'] = place.split(',')[1].strip().split()[1].strip()
                    item['country'] = "United States" 
                    item['phone_number'] = self.validate(store.xpath('.//div[@class="clinic-phone"]/a/text()'))
                    item['store_hours'] = store.xpath('.//div[@class="clinic-hours"]/text()').extract()[1].strip().replace("Today's Hours:", '').strip()
                    #item['store_type'] = info_json["@type"]
                    item['other_fields'] = ""
                    item['coming_soon'] = 0
                    detail_url = 'https://www.thejoint.com' + self.validate(store.xpath('.//div[@class="clinic-directions"]/a/@href'))
                    request = scrapy.Request(url=detail_url, callback=self.parse_lat_lng) 
                    request.meta['item'] = item
                    yield request
            except:
                pdb.set_trace()
                pass

        def parse_lat_lng(self, response):
            try:
                item = response.meta['item']
                item['latitude'] = response.body.split('data-latitude="')[1].split('"')[0]
                item['longitude'] = response.body.split('data-longitude="')[1].split('"')[0]
                yield item      
            except:
                pdb.set_trace()
                pass

        def parse_hour(self, response):
            try:
                store = yaml.load(response.body.split("var locationList = '")[-1].split('},]}')[0] + '},]}')['locationData'][0]
                item = response.meta['item']
                item['store_hours'] = store['LobbyHour']
                yield item
            except:
                pdb.set_trace()
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




