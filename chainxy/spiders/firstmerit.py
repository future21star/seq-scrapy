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

class FirstmeritSpider(scrapy.Spider):
    name = 'firstmerit'
    # you can set the user agent either in the settings or the spider
    uid_list = []

    headers = {
        "Accept":"application/json, text/javascript, */*; q=0.01",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With":"XMLHttpRequest"
    }

    def start_requests(self):
        url = "https://www.huntington.com/"
        form_data = {
            "longitude":"-83.0008326",
            "latitude":"39.9610692",
            "typeFilter":"1,2",
            "envelopeFreeDepositsFilter":"false",
            "timeZoneOffset":"-480",
            "scController":"GetLocations",
            "scAction":"GetLocationsList"
        }
        yield FormRequest(url=url, formdata=form_data, headers=self.headers, callback=self.parse_store)

    def parse_store(self, response):
        stores = json.loads(response.body)['features']
        for store in stores:
            item = ChainItem()
            item['store_name'] = store["properties"]['LocName']
            item['store_number'] = ""
            item['address'] = store["properties"]['LocStreet']
            item['address2'] = ""
            item['city'] = store["properties"]["LocCity"]
            item['state'] = store["properties"]["LocState"]
            item['zip_code'] = store["properties"]["LocZip"]
            item['country'] = "United States"
            item['phone_number'] = store['properties']['LocPhone']
            item['latitude'] = store["geometry"]['coordinates'][0]
            item['longitude'] = store["geometry"]['coordinates'][1]
            item['store_hours'] = "Sunday:" + store['properties']['SundayLobbyHours'] + ";" + "Monday:" + store['properties']['MondayLobbyHours'] + ";" + "Tuesday:" + store['properties']['TuesdayLobbyHours'] + ";" + "Wednesday:" + store['properties']['WednesdayLobbyHours'] + ";" + "Thursday:" + store['properties']['ThursdayLobbyHours'] + ";" + "Friday:" + store['properties']['FridayLobbyHours'] + ";" + "Saturday:" + store['properties']['SaturdayLobbyHours'] + ";" 
            item['store_type'] = store['properties']['LocType']
            item['other_fields'] = ""
            item['coming_soon'] = 0
            yield item

    def validate(self, xpath_obj):
        try:
            return xpath_obj.extract_first().strip().encode('utf8').replace('\xc3\xb4', 'o').replace("&#39", "'").replace('&amp;nbsp;', '').replace('&nbsp;', '')
        except:
            return ""