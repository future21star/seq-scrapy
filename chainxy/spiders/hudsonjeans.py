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

class HudsonjeansSpider(scrapy.Spider):
    name = 'hudsonjeans'
    # you can set the user agent either in the settings or the spider

    headers = {
        "X-Requested-With":"XMLHttpRequest"
    }
    def start_requests(self):
        URL = 'https://www.hudsonjeans.com/slocator/json/search/'
        form_data = {
            'country' : "US",
        }
        # no need for dont_filter
        yield FormRequest(url=URL, formdata=form_data, headers=self.headers, callback=self.parse_store)

    def parse_store(self, response):
        stores = json.loads(response.body)['maps']['items']
        for store in stores:
            item = ChainItem()
            item['store_number'] = store["entity_id"]
            item['store_name'] = ""
            item['address'] = store["street"]
            item['address2'] = store['street2']
            item['city'] = store["city"]
            zip_code = etree.HTML(store['content'])
            item['state'] = zip_code.xpath('//span[@class="state"]/text()')[0]
            item['zip_code'] = store["postal_code"]
            item['country'] = "United States" 
            item['phone_number'] = str(store["phone"]).split()[0].replace('.', '-')
            if item['phone_number'] == 'None':
                item['phone_number'] = ""
            item['store_hours'] = ""
            item['coming_soon'] = 0
            item['latitude'] = store["latitude"]
            item['longitude'] = store["longitude"]
            item['other_fields'] = ""
            #item['store_type'] = info_json["@type"]
            yield item