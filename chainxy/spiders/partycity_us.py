
import scrapy
import json
import os
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from chainxy.items import ChainItem
from lxml import etree
import pdb

class PartycityUSSpider(scrapy.Spider):
    name = 'partycity_us'
    domain = 'http://stores.partycity.com/'
    history = ['']

    def start_requests(self):
        url = 'http://stores.partycity.com/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        state_list = response.xpath('//div[@class="rio-domainlist"]/a/@href').extract()
        for state in state_list : 
            yield scrapy.Request(url=state, callback=self.parse_state)

    def parse_state(self, response):
        store_list = response.xpath('//div[@class="rio-regionlist"]/a/@href').extract()  
        for store in store_list :
            yield scrapy.Request(url=store, callback=self.parse_store)
    
    def parse_store(self, response):
        item = ChainItem()
        item['store_name'] = " ".join(response.xpath('//div[@class="rio-citylist-locName"]/a/text()').extract())
        item['store_number'] = self.validate(response.xpath('//div[@class="rio-citylist-fid"]/text()')).split('#')[-1].strip()
        item['address'] = self.validate(response.xpath("//div[@class='rio-citylist-addr']/span/text()"))
        item['address2'] = ''
        addr = response.xpath("//div[@class='rio-citylist-addr2']//text()").extract()
        item['city'] = addr[0].strip()
        item['state'] = addr[2].strip()
        item['zip_code'] = addr[3].strip()
        item['country'] = "Canada"
        item['phone_number'] = self.validate(response.xpath("//div[@class='rio-citylist-phone']/text()"))
        lat_lng = self.validate(response.xpath('//a[contains(@href, "https://maps.google.com/maps?ll")]/@href'))
        start_pos = response.body.find('"lat":') + 6 
        item['latitude'] = response.body[start_pos:].split(',')[0]
        start_pos = response.body.find('"lng":') + 6 
        item['longitude'] = response.body[start_pos:].split(',')[0]
        hours = response.xpath('//div[@class="day-hour-row"]/meta/@content').extract()
        item['store_hours'] = ";".join(hours)
        item['store_type'] = ''
        item['other_fields'] = ''
        item['coming_soon'] = '0'
        yield item

    def validate(self, xpath):
        try:
            return xpath.extract_first().strip()
        except:
            return ""