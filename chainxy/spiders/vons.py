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

class VonsSpider(scrapy.Spider):
    name = "vons"
    uid_list = []
    start_urls = ['http://locator.safeway.com/ajax?&xml_request=%3Crequest%3E%3Cappkey%3EC8EBB30E-9CDD-11E0-9770-6DB40E5AF53B%3C%2Fappkey%3E%3Cformdata+id%3D%22locatorsearch%22%3E%3Cevents%3E%3Cwhere%3E%3Ceventstartdate%3E%3Cge%3Enow()%3C%2Fge%3E%3C%2Feventstartdate%3E%3C%2Fwhere%3E%3Climit%3E2%3C%2Flimit%3E%3C%2Fevents%3E%3Cdataview%3Estore_default%3C%2Fdataview%3E%3Cgeolocs%3E%3Cgeoloc%3E%3Caddressline%3E%3C%2Faddressline%3E%3Clongitude%3E-91.72485351562497%3C%2Flongitude%3E%3Clatitude%3E30.694611546632274%3C%2Flatitude%3E%3Ccountry%3EUS%3C%2Fcountry%3E%3C%2Fgeoloc%3E%3C%2Fgeolocs%3E%3Csearchradius%3E5000%3C%2Fsearchradius%3E%3Cstateonly%3E1%3C%2Fstateonly%3E%3Climit%3E3000%3C%2Flimit%3E%3Cwhere%3E%3Ccountry%3EUS%3C%2Fcountry%3E%3Cclosed%3E%3Cdistinctfrom%3E1%3C%2Fdistinctfrom%3E%3C%2Fclosed%3E%3Cfuelparticipating%3E%3Cdistinctfrom%3E1%3C%2Fdistinctfrom%3E%3C%2Ffuelparticipating%3E%3Cbakery%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fbakery%3E%3Cdeli%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fdeli%3E%3Cfloral%3E%3Ceq%3E%3C%2Feq%3E%3C%2Ffloral%3E%3Cliquor%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fliquor%3E%3Cmeat%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fmeat%3E%3Cpharmacy%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fpharmacy%3E%3Cproduce%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fproduce%3E%3Cjamba%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fjamba%3E%3Cseafood%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fseafood%3E%3Cstarbucks%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fstarbucks%3E%3Cvideo%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fvideo%3E%3Cfuelstation%3E%3Ceq%3E%3C%2Feq%3E%3C%2Ffuelstation%3E%3Cdvdplay_kiosk%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fdvdplay_kiosk%3E%3Ccoinmaster%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fcoinmaster%3E%3Cwifi%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fwifi%3E%3Cbank%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fbank%3E%3Cseattlesbestcoffee%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fseattlesbestcoffee%3E%3Cbeveragestewards%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fbeveragestewards%3E%3Cphoto%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fphoto%3E%3Cwu%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fwu%3E%3Cdebi_lilly_design%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fdebi_lilly_design%3E%3Cdelivery%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fdelivery%3E%3Cfresh_cut_produce%3E%3Ceq%3E%3C%2Feq%3E%3C%2Ffresh_cut_produce%3E%3C%2Fwhere%3E%3C%2Fformdata%3E%3C%2Frequest%3E']

    def parse(self, response):
        response = etree.HTML(response.body)
        stores = response.xpath('//poi')
        for store in stores:
            item = ChainItem()
            if '-' in self.validate(store.xpath('.//displayname/text()')):
                try:
                    num = int(self.validate(store.xpath('.//displayname/text()')).split('-')[-1].strip())
                except:
                    num = ""                     
                item['store_number'] = num
                item['store_name'] = self.validate(store.xpath('.//displayname/text()')).split('-')[0].strip()
            else:
                item['store_number'] = ""
                item['store_name'] = self.validate(store.xpath('.//displayname/text()'))
            item['address'] = self.validate(store.xpath('.//address1/text()'))
            item['address2'] = self.validate(store.xpath('.//address2/text()'))
            item['city'] = self.validate(store.xpath('.//city/text()'))
            item['state'] = self.validate(store.xpath('.//state/text()'))
            item['zip_code'] = self.validate(store.xpath('.//postalcode/text()'))
            item['country'] = "United States" 
            item['phone_number'] = self.validate(store.xpath('.//phone/text()'))
            if item['zip_code'] == "19810":
                pdb.set_trace()
            item['store_hours'] = self.validate(store.xpath('.//storehours1/text()')).replace("<br/>", ";").replace("<br />", ";")
            item['latitude'] = self.validate(store.xpath('.//latitude/text()'))
            item['longitude'] = self.validate(store.xpath('.//longitude/text()'))
            #item['store_type'] = info_json["@type"]
            item['other_fields'] = ""
            if self.validate(store.xpath('.//comingsoon_flag/text()')) == "1":
                item['coming_soon'] = self.validate(store.xpath('.//comingsoon_flag/text()'))
            else:
                item['coming_soon'] = 0
            yield item
        # except:
            # pass            

    def validate(self, xpath):
        try:
            return self.replaceUnknownLetter(xpath[0].strip())
        except:
            return ""

    def isEndWithZipCode(self, str):
        str = str[-5:]
        count = 0
        if str[0].isdigit():
            for char in str:
                if char.isdigit():
                    count += 1
            if count == 5:
                return True
        str = str[-3:]
        if (str[0].isdigit() and (not str[1].isdigit()) and str[2].isdigit()):
            return True            
        return False

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




