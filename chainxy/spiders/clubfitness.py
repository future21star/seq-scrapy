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

class ClubfitnessSpider(scrapy.Spider):
    name = "clubfitness"
    uid_list = []
    start_urls = ['http://www.clubfitness.us/locations/']

    def parse(self, response):
        stores = self.getInfo(response)["KOObject"][0]["locations"]
        for store in stores:
            item = ChainItem()
            item['store_number'] = ""
            item['store_name'] = store["title"].strip()
            addr = etree.HTML(store["address"].strip())
            addr = addr.xpath('//text()')
            item['address'] = " ".join(addr[:-1]).strip()
            item['address2'] = ""
            try:
                item['city'] = addr[-1].split(',')[0].strip()
                item['state'] = addr[-1].split(',')[1].split()[0].strip()
                item['zip_code'] = addr[-1].split(',')[1].split()[1].strip()
            except:
                item['state'] = addr[-2].split(',')[-1].strip()
                item['zip_code'] = addr[-1].strip()
                item['city'] = addr[-2].split(',')[0].strip()
            item['country'] = "United States"
            description = etree.HTML(store["description"].strip())
            description = description.xpath('//div[@class="location"]/text()')
            try:
                item['phone_number'] = self.validatePhoneNumber(description[1])
            except:
                item['phone_number'] = ""
            item['store_hours'] = ""
            item['latitude'] = store["latitude"].strip()
            item['longitude'] = store["longitude"].strip()
            #item['store_type'] = info_json["@type"]
            item['other_fields'] = ""
            if 'Coming Soon' in store["title"]:
                item['coming_soon'] = 1
            else:
                item['coming_soon'] = 0
            url = store["locationUrl"].strip()
            request = scrapy.Request(url=url, callback=self.parse_hour)
            request.meta['item'] = item
            yield request
        # except:
            # pass            

    def parse_hour(self, response):
        item = response.meta['item']
        item['store_hours'] = ""
        for hour in response.xpath('//ul[@class="class-hours"][1]/li'):
            hour_value = hour.xpath('.//text()').extract()
            hour_value = [a.strip() for a in hour_value if a.strip() != ""]
            item['store_hours'] += hour_value[0] + ":" + hour_value[1] + ";"
        yield item
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
        pos = body.find("var maplistScriptParamsKo = ") + 28
        dest = ""
        while body[pos: pos+2] != "};":
            dest += body[pos]
            pos += 1
        dest += "}"
        return json.loads(dest)

    def validatePhoneNumber(self, phone_number):
        return phone_number.strip().replace('.', '-')        