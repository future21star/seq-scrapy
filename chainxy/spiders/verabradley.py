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

class VerabradleySpider(scrapy.Spider):
    name = "verabradley"
    uid_list = []
    start_urls = ['https://www.verabradley.com/us/selfservice/FindStore']

    def parse(self, response):
        for page in range(1, int(response.xpath('//span[@class="total-results"]/text()').extract_first().strip()) / 10 + 1):
            url = "https://www.verabradley.com/us/selfservice/FindStore?zip=&address=&city=&state=&curpage=%s" % str(page)
            yield scrapy.Request(url=url, callback=self.parse_store)

    def parse_store(self, response):
        # try:
        stores = response.xpath('//div[contains(@class, "store-result")]')
        for store in stores:
            item = ChainItem()
            item['store_number'] = self.validate(store.xpath('.//a[contains(@href, "/us/selfservice/storeDetail?storeItem=bbStr")]/@href')).split("bbStr")[-1]
            item['store_name'] = self.validate(store.xpath('.//span[@class="store-name-text"]/text()'))
            item['address'] = self.validate(store.xpath('.//span[@itemprop="addressLocality"]/text()'))
            item['address2'] = ""
            item['city'] = self.validate(store.xpath('.//span[@itemprop="addressRegion"][1]/text()'))[:-1]
            item['state'] = self.validate(store.xpath('.//span[@itemprop="addressRegion"][2]/text()'))
            item['zip_code'] = self.validate(store.xpath('.//span[@itemprop="postalCode"]/text()'))
            item['country'] = "United States" 
            item['phone_number'] = self.validate(store.xpath('.//span[@itemprop="telephone"]/text()'))[7:].strip()
            item['store_hours'] = ""
            item['latitude'] = self.validate(store.xpath('./@data-lat'))
            item['longitude'] = self.validate(store.xpath('./@data-long'))
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




