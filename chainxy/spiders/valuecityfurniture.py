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

class ValuecityfurnitureSpider(scrapy.Spider):
    name = "valuecityfurniture"
    uid_list = []
    start_urls = ['https://www.valuecityfurniture.com/store-locator/show-all-locations']

    def parse(self, response):
        # try:
            stores = response.xpath('//div[contains(@class, "store-locator-stores-result-list-item")]')
            for store in stores:
                item = ChainItem()
                item['store_number'] = ""
                item['store_name'] = self.validate(store.xpath('.//strong[@class="sl-storename"]/text()'))
                item['address'] = self.validate(store.xpath('.//span[@itemprop="streetAddress"]/text()'))
                item['address2'] = ""
                item['city'] = self.validate(store.xpath('.//span[@itemprop="addressLocality"]/text()'))
                item['state'] = self.validate(store.xpath('.//span[@itemprop="addressRegion"]/text()'))
                item['zip_code'] = self.validate(store.xpath('.//span[@itemprop="postalCode"]/text()'))
                item['country'] = "United States" 
                item['phone_number'] = self.validate(store.xpath('.//span[@itemprop="telephone"]/text()'))
                hours = store.xpath('.//div[@class="store-hours-table"]//text()').extract()
                hours = [a.strip() for a in hours if a.strip() != ""]
                item['store_hours'] = ""
                for hour in hours:
                    if (hours.index(hour) % 2 == 0):
                        item['store_hours'] = hour + ":"
                    else:
                        item['store_hours'] = hour + ";"
                item['latitude'] = ""
                item['longitude'] = ""
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




