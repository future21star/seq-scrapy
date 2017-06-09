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
import usaddress

class FitnessheadquartersSpider(scrapy.Spider):
    name = "fitnessheadquarters"
    uid_list = []
    start_urls = ['http://www.fitnessheadquarters.com/store_locations.asp']
    domain = "http://www.fitnessfactorygym.com/"

    def parse(self, response):
        try:
            stores = response.xpath('//center/table[1]/tr[2]//table[1]/tr[5]//table[1]/tr[2]/td[1]/table[1]/tr[1]/td[1]/table[1]/tr')
            for store in stores:
                item = ChainItem()
                item['store_number'] = ""
                if self.validate(store.xpath('.//span[@itemprop="name"]/strong/text()')) == "":
                    item['store_name'] = self.validate(store.xpath('./td[1]/strong/text()'))
                    _addr = store.xpath('./td[1]/text()').extract()[2].strip()
                    if _addr == "":
                        _addr = store.xpath('./td[1]/text()').extract()[1].strip()
                    addr = usaddress.parse(_addr.strip())
                    item['address'] = item['address2'] = item['city'] = item['zip_code'] = item['state'] = ""
                    for temp in addr:
                        if temp[1] == 'PlaceName':
                            item['city'] = temp[0].replace(',', '')
                        elif temp[1] == 'StateName':
                            item['state'] = temp[0].replace(',', '')
                        elif temp[1] == 'ZipCode':
                            item['zip_code'] = temp[0].replace(',', '')
                    item['address'] = _addr.replace(',', '').replace(item['city'], '').replace(item['state'],'').replace(item['zip_code'],'').strip()                           
                    hours = store.xpath('./td[1]/div/text()').extract()
                else:
                    item['store_name'] = self.validate(store.xpath('.//span[@itemprop="name"]/strong/text()'))
                    item['address'] = self.validate(store.xpath('.//span[@itemprop="street-address"]/text()'))
                    item['city'] = self.validate(store.xpath('.//span[@itemprop="locality"]/text()'))
                    item['state'] = self.validate(store.xpath('.//span[@itemprop="region"]/text()'))
                    item['zip_code'] = store.xpath('./td[1]/div[1]/text()').extract()[4].strip()
                    hours = store.xpath('./td[1]/div[1]/div[2]/text()').extract()
                item['address'] = item['address'].replace('Ft.', "").replace('Blvd.', 'Southlake Blvd.')
                item['city'] = item['city'].replace('Worth', "Fort Worth")
                item['address2'] = ""
                item['country'] = "United States"
                item['phone_number'] = self.validate(store.xpath('./td[2]/text()')).replace('Ph:', '').strip()
                hours = [a.strip() for a in hours if a.strip() != ""]
                item['store_hours'] = ";".join(hours[1:]).replace("&;Store Hours:;", "")
                try:
                    lat_lng = self.validate(store.xpath('./td[1]//a[1]/@href')).split('sll=')[1]
                except:
                    lat_lng = self.validate(store.xpath('./td[1]//a[1]/@href')).split('ll=')[1]
                item['latitude'] = lat_lng.split(',')[0]
                item['longitude'] = lat_lng.split(',')[1].split('&')[0]
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




