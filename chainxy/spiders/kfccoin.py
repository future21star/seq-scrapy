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

class KfccoinSpider(scrapy.Spider):
    name = 'kfccoin'
    # you can set the user agent either in the settings or the spider
    uid_list = []

    headers = {
        "Accept":"application/json, text/javascript, */*; q=0.01",
        "x-newrelic-id": "VQACWFJRARAFV1NbBwYFVg==",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With":"XMLHttpRequest"
    }
    start_urls = ["https://online.kfc.co.in/store-locator"]

    def parse(self, response):
        cities = response.xpath('//select[@id="store_loc_city_combobox"]/option')
        for city in cities:
            city_value = city.xpath('./@value').extract_first()
            url = "https://online.kfc.co.in/ajax-store-locator"
            form_data = {
                "city":city_value,
            }
            yield FormRequest(url=url, formdata=form_data, headers=self.headers, callback=self.parse_city)

    def parse_city(self, response):
        stores = json.loads(response.body)
        for store in stores:
            entity_id = store["entity_id"]
            url = "https://online.kfc.co.in/ajax-store-locator-lang-lat"
            form_data = {
                "store": entity_id
            }
            yield FormRequest(url=url, formdata=form_data, headers=self.headers, callback=self.parse_store)

    def parse_store(self, response):
        store = json.loads(response.body)[0]
        item = ChainItem()
        item['store_name'] = ""
        item['store_number'] = ""
        item['address'] = store["field_store_building_name_number_value"]
        item['address2'] = ""
        item['city'] = store["field_store_city_value"]
        item['state'] = ""
        item['zip_code'] = ""
        item['country'] = "India"
        if store['field_store_contact_number_value'] == None:
            item['phone_number'] = ""
        else:
            item['phone_number'] = store['field_store_contact_number_value']
        item['latitude'] = store["field_store_latitude_value"]
        item['longitude'] = store["field_store_longitude_value"]
        if store["field_store_timing_value"] == None:
            item['store_hours'] = ""
        else:
            item['store_hours'] = store["field_store_timing_value"].replace("to", "-")
        item['store_type'] = ""
        item['other_fields'] = ""
        item['coming_soon'] = 0
        yield item
            
    def validate(self, xpath_obj):
        try:
            return xpath_obj.extract_first().strip().encode('utf8').replace('\xc3\xb4', 'o').replace("&#39", "'").replace('&amp;nbsp;', '').replace('&nbsp;', '')
        except:
            return ""