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
import usaddress

class SpicypickleSpider(scrapy.Spider):
    name = "spicypickle"
    uid_list = []
    start_urls = ["http://www.spicypickle.com/restaurants/"]

    def parse(self, response):
        try:
            stores = response.xpath('//div[@class="sqs-block html-block sqs-block-html"]/div[@class="sqs-block-content"]')
            for store in stores:
                item = ChainItem()
                item['store_number'] = ""
                item['store_name'] = self.validate(store.xpath('./h1/strong/text()'))
                addr = store.xpath('./p[1]/text()').extract()
                item['address'] = addr[0]
                item['address2'] = ""
                item['city'] = addr[1].split(',')[0].strip()
                item['state'] = addr[1].split(',')[1].strip().split()
                item['zip_code'] = addr[2].strip()
                item['country'] = "Canada"
                item['phone_number'] = self.validate(store.xpath('.//div[@class="x-visibility x-hidden-phone"]/a/text()'))
                hours = store.xpath('.//div[@class="x-column x-sm vc x-1-4"][1]/p//text()').extract()
                hours = [a.strip() for a in hours if a.strip() != ""]
                item['store_hours'] = ""
                for hour in hours[:-1]:
                    if hours.index(hour) % 2 == 0:
                        item['store_hours'] += hour + ":"
                    else:
                        item['store_hours'] += hour + ";"
                item['latitude'] = response.body.split('lat&quot;:&quot;')[1].split('&')[0]
                item['longitude'] = response.body.split('lng&quot;:&quot;')[1].split('&')[0]
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




