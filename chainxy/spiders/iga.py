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
import yaml

class IgaSpider(scrapy.Spider):
	name = "iga"
	uid_list = []

	def start_requests(self):
		headers = {
		"Accept":"*/*",
		"Accept-Encoding":"gzip, deflate",
		"Accept-Language":"en-GB,en-US;q=0.8,en;q=0.6",
		"Connection":"keep-alive",
		"Content-Type":"text/plain; charset=UTF-8",
		"X-AjaxPro-Method":"GetStorePins",
		}
		form_datas = [
		'{"srl":{"MinLong":"-67.18764701562498","MaxLong":"-52.026514203124975","MinLat":"45.41569287852881","MaxLat":"52.67128950037055","ZoomLevel":6},"pinType":"1"}',
		'{"srl":{"MinLong":"-81.18422904687498","MaxLong":"-66.02309623437498","MinLat":"43.70946398971876","MaxLat":"51.19473686018495","ZoomLevel":6},"pinType":"1"}',
		'{"srl":{"MinLong":"-81.03042045312498","MaxLong":"-65.86928764062498","MinLat":"39.64153017921161","MaxLat":"47.652330681043054","ZoomLevel":6},"pinType":"1"}'
		]
		url = "http://myirving.com/ajaxpro/StationWebsites.SharedContent.Web.Common.Controls.Map.StoreData,StationWebsites.ashx"
		for form_data in form_datas:
			yield  scrapy.Request(url=url, method="POST", body=form_data, headers=headers, callback=self.parse_store)

	def parse_store(self, response):
		try:
			stores = json.loads(response.body)["value"]["Payload"]
			for _store in stores:
				store = _store["Store"]
				item = ChainItem()
				item['store_number'] = store["CorporateId"]
				item['store_name'] = store["DisplayName"]
				item['address'] = store["Address"]
				item['address2'] = ""
				item['city'] = store["City"]
				item['state'] = store["State"]
				item['zip_code'] = store["Zip"]
				item['latitude'] = store["Latitude"]
				item['longitude'] = store["Longitude"]
				item['country'] = store["Country"]
				item['phone_number'] = _store["PrimaryPhoneNumber"]
				item['store_hours'] = ""
				item['other_fields'] = ""
				item['coming_soon'] = 0
				request = scrapy.Request(url=_store["StoreURL"], callback=self.parse_hour)
				if item['store_number'] in self.uid_list:
					continue
				self.uid_list.append(item['store_number'])
				request.meta['item'] = item
				yield request
		except:
			pdb.set_trace()
			pass            

	def parse_hour(self, response):
		try:
			item = response.meta['item']
			hours = response.xpath("//div[@class='store-hours-container-div']//text()").extract()
			hours = [a.strip() for a in hours if a.strip() != ""]
			item['store_hours'] = " ".join(hours)
			yield item
		except:
			pdb.set_trace()
			pass
    # def validate(self, xpath):
    #     try:
    #         return self.replaceUnknownLetter(xpath.extract_first().strip())
    #     except:
    #         return ""

    # def replaceUnknownLetter(self, source):
    #     try:
    #         formatted_value = source.encode('utf8').replace('\xc3', '').replace('\xa9', 'e').replace('\xa8', 'e').replace('\xb4', 'o').replace('\xb3', 'o').replace('\xb9', 'u').replace('\xba', 'u').replace('\x89', 'E').replace('\xaa', 'e').replace('\x89', 'E').replace('\xa2', 'a').replace('\xac', 'i').replace('\xad', 'i').replace('\xae', 'i')
    #         # if "x8" in formatted_value or "x9" in formatted_value or "xa" in formatted_value or "xb" in formatted_value:
    #         #   pdb.set_trace()
    #         return formatted_value
    #     except:
    #         return source
    
    # def format(self, item):
    #     try:
    #         return unicodedata.normalize('NFKD', item).encode('ascii','ignore').strip()
    #     except:
    #         return ''           

    # def getInfo(self, response):
    #     body = response.body
    #     pos = body.find("var markerData = ") + 18
    #     stores = "[]"
    #     store = ""
    #     while body[pos: pos+2] != "];":
    #         if body[pos] == "[":
    #             store = ""
    #         if body[pos] == "]":
    #             store += "]"
    #             stores.append(store)
    #         store += body[pos]
    #         pos += 1
    #     return stores

    # def validatePhoneNumber(self, phone_number):
    #     return phone_number.strip().replace('.', '-')        