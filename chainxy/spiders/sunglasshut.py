
import scrapy
import json
import os
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from chainxy.items import ChainItem
from lxml import etree

class SunglasshutSpider(scrapy.Spider):
    name = 'sunglasshut'
    domain = 'http://stores.sunglasshut.com/'
    history = ['']

    def start_requests(self):
        url = 'http://stores.sunglasshut.com'
        yield scrapy.Request(url=url, callback=self.parse_state)

    def parse_state(self, response):
        state_list = response.xpath('//li[@class="c-directory-list-content-item"]')
        for state in state_list : 
            go_url = state.xpath('.//a/@href').extract_first()
            state_link = self.domain + go_url
            if len(go_url.split('/')) == 2 :
                yield scrapy.Request(url=state_link, callback=self.parse_store)
            else :
                yield scrapy.Request(url=state_link, callback=self.parse_city)

    def parse_city(self, response):
        city_list = response.xpath('//li[@class="c-directory-list-content-item"]')  
        for city in city_list :
            go_url = city.xpath('.//a/@href').extract_first()
            city_link = self.domain + go_url
            if len(go_url.split('/')) == 4 :
                yield scrapy.Request(url=city_link, callback=self.parse_detail)
            else :
                yield scrapy.Request(url=city_link, callback=self.parse_store)
    
    def parse_store(self, response):
        store_list = response.xpath('//a[@class="c-location-grid-item-link"]')
        for store in store_list:
            store_link = self.domain + store.xpath('./@href').extract_first()[3:]
            print store_link
            yield scrapy.Request(url=store_link, callback=self.parse_detail)

    def parse_detail(self, response):
        detail = response.xpath(".//div[contains(@class, 'col-sm-6 col-flex-sm info-col')]")
        item = ChainItem()
        item['store_name'] = response.xpath('.//h1[@id="location-name"]/div/text()').extract_first().strip()
        item['store_number'] = ''
        item['address'] = detail.xpath(".//div[@id='address']/span[contains(@class, 'c-address-street c-address-street-1')]/text()").extract_first().strip()
        item['address2'] = ''
        item['city'] = detail.xpath(".//div[@id='address']/span[contains(@class, 'c-address-city')]/span/text()").extract_first().replace(',','').strip()
        item['state'] = detail.xpath('.//div[@id="address"]/span[contains(@class, "c-address-state")]/text()').extract_first().strip()
        item['zip_code'] = detail.xpath('.//div[@id="address"]/span[contains(@class, "c-address-postal-code")]/text()').extract_first().strip()
        item['country'] = detail.xpath('.//div[@id="address"]/span[1]/text()').extract_first().strip()
        if item['country'] == 'US':
            item['country'] = 'United States'
        item['phone_number'] = detail.xpath('.//span[@id="telephone"]/text()').extract_first().strip()
        item['latitude'] = detail.xpath('.//meta[@itemprop="latitude"]/@content').extract_first().strip()
        item['longitude'] = detail.xpath('.//meta[@itemprop="longitude"]/@content').extract_first().strip()

        h_temp = ''
        hour_list = response.xpath('.//table[@class="c-location-hours-details"]//tbody//tr')
        for hour in hour_list : 
            weekday = hour.xpath('.//td[@class="c-location-hours-details-row-day"]/text()').extract_first()
            weektime = ''
            weektime_list = hour.xpath('.//td[@class="c-location-hours-details-row-intervals"]//div//span')
            if len(weektime_list) == 3:
                for time in weektime_list : 
                    weektime = weektime + time.xpath('./text()').extract_first()
            h_temp = h_temp + weekday + weektime + ' ; '
        item['store_hours'] = h_temp[:-3]
        item['store_type'] = ''
        item['other_fields'] = ''
        item['coming_soon'] = '0'
        if item['phone_number'] not in self.history:
            yield item
            self.history.append(item['phone_number'])
