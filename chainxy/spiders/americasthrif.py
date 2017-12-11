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

class AmericasthrifSpider(scrapy.Spider):
    name = 'americasthrif'
    # you can set the user agent either in the settings or the spider
    uid_list = []

    headers = {
        "Content-Type":"application/x-www-form-urlencoded",
        "X-Requested-With":"XMLHttpRequest"        
    }

    def start_requests(self):
        url = "http://www.americasthrift.com/wp-admin/admin-ajax.php"
        form_data = {
            "action" : "get_dropboxes"
        }
        yield FormRequest(url=url, formdata=form_data, headers=self.headers, callback=self.parse_store)

    def parse_store(self, response):
        stores = json.loads(response.body)
        for store in stores:
            item = ChainItem()
            item['store_name'] = store["store_name"]
            item['store_number'] = ""
            item['address'] = store["box_address"]
            item['address2'] = ""
            item['city'] = store["box_city"]
            item['state'] = store["box_state"]
            item['zip_code'] = store["box_zip"]
            item['country'] = "United States"
            item['phone_number'] = ""
            item['latitude'] = store["latitude"]
            item['longitude'] = store["longitude"]
            
            item['state'] = store["box_state"]
            item['zip_code'] = store["box_zip"]
            item['country'] = "United States"
            item['phone_number'] = ""
            item['latitude'] = store["latitude"]
            item['longitude'] = store["longitude"]
            
            item['store_hours'] = ""
            #item['store_type'] = info_json["@type"]
            item['other_fields'] = ""
            item['coming_soon'] = 0
            yield item

    def validate(self, xpath_obj):
        try:
            return xpath_obj.extract_first().strip().encode('utf8').replace('\xc3\xb4', 'o').replace("&#39", "'").replace('&amp;nbsp;', '').replace('&nbsp;', '')
        except:
            return ""
        
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

class AmericasthrifSpider(scrapy.Spider):
    name = 'americasthrif'
    # you can set the user agent either in the settings or the spider
    uid_list = []

    headers = {
        "Content-Type":"application/x-www-form-urlencoded",
        "X-Requested-With":"XMLHttpRequest"        
    }

    def start_requests(self):
        url = "http://www.americasthrift.com/wp-admin/admin-ajax.php"
        form_data = {
            "action" : "get_dropboxes"
        }
        yield FormRequest(url=url, formdata=form_data, headers=self.headers, callback=self.parse_store)

    def parse_store(self, response):
        stores = json.loads(response.body)
        for store in stores:
            item = ChainItem()
            item['store_name'] = store["store_name"]
            item['store_number'] = ""
            item['address'] = store["box_address"]
            item['address2'] = ""
            item['city'] = store["box_city"]
            item['state'] = store["box_state"]
            item['zip_code'] = store["box_zip"]
            item['country'] = "United States"
            item['phone_number'] = ""
            item['latitude'] = store["latitude"]
            item['longitude'] = store["longitude"]
            item['store_hours'] = ""
            #item['store_type'] = info_json["@type"]
            item['other_fields'] = ""
            item['coming_soon'] = 0
            yield item

    def validate(self, xpath_obj):
        try:
            return xpath_obj.extract_first().strip().encode('utf8').replace('\xc3\xb4', 'o').replace("&#39", "'").replace('&amp;nbsp;', '').replace('&nbsp;', '')
        except:
            return ""
