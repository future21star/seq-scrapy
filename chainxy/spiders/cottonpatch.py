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

class CottonpatchSpider(scrapy.Spider):
    name = "cottonpatch"
    uid_list = []
    start_urls = ['http://www.cottonpatch.com/locations/xmls/all.xml']
    domain = "http://www.cottonpatch.com"

    def parse(self, response):
        stores = response.xpath('//marker')
        for store in stores:
            html = etree.HTML(store.xpath('./@html').extract_first())
            href = html.xpath("//a[contains(@href, '../locations/')]/@href")[0]
            url = self.domain + href[2:]
            request = scrapy.Request(url=url, callback=self.parse_store)
            item = ChainItem()
            item['latitude'] = store.xpath('./@lat').extract_first()
            item['longitude'] = store.xpath('./@lng').extract_first()
            request.meta['item'] = item
            yield request
    def parse_store(self, response):
        try:
            item = response.meta['item']
            addr = response.xpath('//p[@class="style8"][1]/text()').extract()
            item['store_number'] = ""
            item['store_name'] = ""
            item['address'] = addr[0].strip()
            item['address2'] = ""
            item['city'] = addr[1].strip().split(',')[0]
            try:
                item['state'] = addr[1].strip().split(',')[1].split()[0]
                try:
                    item['zip_code'] = addr[1].strip().split(',')[1].split()[1]
                except:
                    item['zip_code'] = ""
            except:
                item['state'] = addr[2].strip().split(',')[1].split()[0]
                try:
                    item['zip_code'] = addr[2].strip().split(',')[1].split()[1]
                except:
                    item['zip_code'] = ""
            item['country'] = "United States"
            item['phone_number'] = self.validate(response.xpath('//p[@class="style8"][1]/span[@class="boxlink"][1]/text()'))
            if 'Phone' in item['phone_number']:
                item['phone_number'] = item['phone_number'].split("Phone")[-1][4:]
            hours = response.xpath('//p[@class="hours-loc"]/text()').extract()
            hours = [a.strip() for a in hours if a.strip() != ""]
            item['store_hours'] = ";".join(hours)
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




