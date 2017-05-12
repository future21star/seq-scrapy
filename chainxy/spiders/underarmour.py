import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class UnderarmourSpider(scrapy.Spider):
    name = "underarmour"
    uid_list = []
    payload = '<request><appkey>24358678-428E-11E4-8BC2-2736C403F339</appkey><formdata id="locatorsearch"><dataview>store_default</dataview><order>UASPECIALITY, UAOUTLET, AUTHORIZEDDEALER, rank,_distance</order><limit>2000</limit><stateonly>1</stateonly><nobf>1</nobf><geolocs><geoloc><addressline>Dallas TX 75205</addressline><longitude>%s</longitude><latitude>%s</latitude><country>US</country></geoloc></geolocs><searchradius>3000</searchradius><where><or><uaspeciality><eq>1</eq></uaspeciality><uaoutlet><eq>1</eq></uaoutlet><authorizeddealer><eq>1</eq></authorizeddealer></or></where></formdata></request>'

    def __init__(self):
        long_lat_fp = open('cities_us.json', 'rb')
        self.long_lat_reader = json.load(long_lat_fp)
    
    def start_requests(self):
        for row in self.long_lat_reader:
            payload = self.payload % (row['longitude'], row['latitude'])         
            yield scrapy.Request(url='https://hosted.where2getit.com/underarmour/2015/ajax?lang=en-EN&xml_request=%s' % payload, callback=self.parse_store)

    # get longitude and latitude for a state by using google map.
    def parse_store(self, response):
        try:
            stores = response.xpath("//poi")
            for store in stores:
                item = ChainItem()
                item['store_name'] = self.validate(store.xpath(".//name/text()"))
                item['store_number'] = self.validate(store.xpath(".//uid/text()"))
                item['address'] = self.validate(store.xpath(".//address1/text()"))
                item['address2'] = self.validate(store.xpath(".//address2/text()"))
                item['phone_number'] = self.validate(store.xpath(".//phone/text()")).strip()
                if item['phone_number'] in ["0", "-"]:
                    item['phone_number'] = ""
                item['city'] = self.validate(store.xpath(".//city/text()"))
                item['state'] = self.validate(store.xpath(".//province/text()"))
                if item['state'] == "":
                    item['state'] = self.validate(store.xpath(".//state/text()"))

                item['zip_code'] = self.validate(store.xpath(".//postalcode/text()"))
                item['country'] = self.validate(store.xpath(".//country/text()"))
                item['latitude'] = self.validate(store.xpath(".//latitude/text()"))
                item['longitude'] = self.validate(store.xpath(".//longitude/text()"))
                item['store_hours'] = self.validate(store.xpath(".//hours/text()"))
                hour2 = self.validate(store.xpath(".//hours2/text()"))
                if hour2 != "":
                    item['store_hours'] += "; " + hour2
                     
                #item['store_type'] = info_json["@type"]
                item['other_fields'] = ""
                item['coming_soon'] = "0"

                if item["store_number"] != "" and item["store_number"] in self.uid_list:
                    return
                self.uid_list.append(item["store_number"])
                yield item
        except:
            pdb.set_trace()
            pass
    # get store info in store detail page
    #def parse_store_content(self, response):
    #    pass

    def validate(self, xpath_obj):
        try:
            return xpath_obj.extract_first().strip()
        except:
            return ""


