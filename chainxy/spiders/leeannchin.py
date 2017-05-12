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

class LeeannchinSpider(scrapy.Spider):
    name = "leeannchin"
    uid_list = []
    start_urls = ['http://www.leeannchin.com//locations/view_all_locations']

    def start_request(self):
        headers = {
            "Accept":"application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"en-GB,en-US;q=0.8,en;q=0.6",
            "Connection":"keep-alive",
            "Content-Length":"0",
            "Cookie":"ci_session=a%3A4%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22107540502aca18bbdd4e902fbb005643%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A10%3A%2261.6.62.53%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A50%3A%22Mozilla%2F5.0+%28X11%3B+Linux+x86_64%29+AppleWebKit%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bs%3A10%3A%221494509430%22%3B%7D4de2b013cc7ddfa98ef5e80c1a7586cd",
            "Host":"www.leeannchin.com",
            "Origin":"http://www.leeannchin.com",
            "Referer":"http://www.leeannchin.com/locations",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest"
        }
        url = "http://www.leeannchin.com//locations/view_all_locations"
        yield FormRequest(url=url, headers=headers, callback=self.parse_store)

    def parse(self, response):
        stores = json.loads(response.body)['locations']
        for store in stores:
            item = ChainItem()
            item['store_number'] = store["locationv2_id"]
            item['store_name'] = ""
            item['address'] = store["address"]
            item['address2'] = ""
            item['city'] = store["city"]
            item['state'] = store["state"]
            item['zip_code'] = store["postal_code"]
            item['country'] = "United States"
            item['phone_number'] = store["phone"].replace('.', '-')
            item['store_hours'] = store["description"].split("<br>")[-1].strip().replace('Hours of operation:', '').strip()
            item['latitude'] = store["lat"]
            item['longitude'] = store["lng"]
            item['other_fields'] = ""
            item['coming_soon'] = 0
            yield item
        # except:
            # pass            

    def validate(self, xpath):
        try:
            return self.replaceUnknownLetter(xpath.extract_first().strip())
        except:
            return ""

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

    def getInfo(self, response):
        body = response.body
        pos = body.find("var GRP_DIN_LOCATIONS = ") + 24
        dest = ""
        while body[pos] != "]":
            dest += body[pos]
            pos += 1
        dest += "]"
        return yaml.load(dest)

    def validatePhoneNumber(self, phone_number):
        return phone_number.strip().replace('.', '-')        