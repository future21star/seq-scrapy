import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem

from selenium import webdriver
from lxml import html
from lxml import etree
import pdb
import time

class ChevysSpider(scrapy.Spider):
    name = "chevys"

    domain = "https://locations.chevys.com/"
    start_urls = ["https://locations.chevys.com/"]

    def __init__(self):
        self.driver = webdriver.Chrome("./chromedriver")

    def parse(self, response):
        self.driver.get("https://locations.chevys.com/")
        time.sleep(2)
        i = 0
        while i != 10:
            self.driver.find_element_by_xpath("//a[@class='leaflet-control-zoom-out']").click()
            time.sleep(0.5)
            i += 1
        source = self.driver.page_source.encode("utf8")
        page = etree.HTML(source)
        for store in page.xpath('//div[@class="col-md-12 location-btn"]'):
            try:
                url = store.xpath('./a[2]/@href')[0]
                yield scrapy.Request(url=url, callback=self.parse_store)
            except:
                pdb.set_trace()
        # self.driver.close()                

    def parse_store(self, response):
        item = ChainItem()
        item['store_name'] = self.validate(response.xpath('//h2[@class="location-title"]/text()'))
        item['store_number'] = ""
        item['address'] = self.validate(response.xpath('//span[@class="number-road"]/text()'))
        item['address2'] = ""
        item['city'] = " ".join(self.validate(response.xpath('//span[@class="city-state-zip"]/text()')).split(',')[:-1]).strip()
        item['state'] = self.validate(response.xpath('//span[@class="city-state-zip"]/text()')).split(',')[-1].strip()
        item['zip_code'] = ""
        item['phone_number'] = self.validate(response.xpath('//span[@class="phone"]/text()')).replace('.', '-')
        item['country'] = "United States"
        lat_lng = self.validate(response.xpath('//div[@id="address"]/a[1]/@href')).split('addr=')[-1]
        item['latitude'] = lat_lng.split(',')[0].strip()
        item['longitude'] = lat_lng.split(',')[-1].strip()
        hours = response.xpath('//div[@id="hours"]/p')
        item['store_hours'] = ""
        for hour in hours:
            hour_value = hour.xpath('.//text()').extract()
            if hour_value[0] == "BAR HOURS":
                break
            try:
                item['store_hours'] += hour_value[0] + ":" + hour_value[1] + ";"
            except:
                item['store_hours'] += ""
        #item['store_type'] = info_json["@type"]
        item['other_fields'] = ""
        item['coming_soon'] = 0
        yield item
    def validate(self, xpath_obj):
        try:
            return xpath_obj.extract_first().strip()
        except:
            return ""

