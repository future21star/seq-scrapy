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

class HessexpressSpider(scrapy.Spider):
    name = "hessexpress"
    uid_list = "[]"
    start_urls = ["https://wfa.kronostm.com/index.jsp?applicationName=SpeedwayLLCNonReqExt&locale=en_US"]

    def parse(self, response):
        for state in response.xpath("//select[@name='search.stateList.value']/option"):
            state_value = state.xpath('./@value').extract_first()
            if state_value != "":
                url = "https://wfa.kronostm.com/index.jsp?applicationName=SpeedwayLLCNonReqExt&locale=en_US"        
                headers = {
                    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Encoding":"gzip, deflate, br",
                    "Accept-Language":"en-GB,en-US;q=0.8,en;q=0.6",
                    "Cache-Control":"max-age=0",
                    "Connection":"keep-alive",
                    "Content-Type":"application/x-www-form-urlencoded",
                    "Cookie":"KTMDWestLB=wIe9zsUNjY0qLmjVyjS/I6odbM2AKMozURgXUAM2pirqNfA9+QDXbNhg+DbCXPRJAe4yjh9x7uY/jtw=; __utmc=2140394; SpeedwayLLCEXT=ESMlrjhZTK8Ap/qTU4nRddZrP3W49f9ehWOCkb5MSE4.; JSESSIONID=SEIRyjy4QBCBbskaD2-URdEy; __utmb=2140394; __utma=2140394.853544452.1494533193.1494553933.1494555824.5; __utmz=2140394.1494555824.4.16.utmccn=(referral)|utmcsr=hessexpress.com|utmcct=/|utmcmd=referral",
                    "Host":"wfa.kronostm.com",
                    "Origin":"https://wfa.kronostm.com",
                    "Referer":"https://wfa.kronostm.com/index.jsp?applicationName=SpeedwayLLCNonReqExt&locale=en_US",
                    "Upgrade-Insecure-Requests":"1",
                    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
                }
                form_data = {
                    "AnchorName_locationSearchCityState":"",
                    "seq":"OneClickLocationSearchResults",
                    "relayData":"%3BM%3FNAAAFHDHCAABDGKGBHGGBCOHFHEGJGMCOEIGBHDGIHEGBGCGMGFBD%3CLAPCFCBEK%3FE%3CIADAAACEGAAAKGMGPGBGEEGGBGDHEGPHCEJAAAJHEGIHCGFHDGIGPGMGEHIHADPEAAAAAAAAAAAAIHHAIAAAAAAALAAAAAAACHEAAAFEJEOEEEFFIHEAAABDAHEAAAPFAEBEHEFEGEMEPFHEPECEKEFEDFEFDHDHCAABBGKGBHGGBCOHFHEGJGMCOEIGBHDGIENGBHAAFAH%3EK%3DB%3DDBGGA%3EBADAAACEGAAAKGMGPGBGEEGGBGDHEGPHCEJAAAJHEGIHCGFHDGIGPGMGEHIHADPEAAAAAAAAAAAAMHHAIAAAAAABAAAAAAAAAHIHI",
                    "event":"com.deploy.application.hourly.plugin.LocationSearch.doSearch",
                    "validateData":"true",
                    "skipRequiredCheck":"false",
                    "search.stateList.value":state_value,
                    "cityList":"",
                    "search.cityList.value":"",
                    "search.cityList.value":"",
                    "search.cityList.value":"",
                    "search.cityList.value":"",
                    "search.cityList.value":"",
                    "search.cityList.value":"",
                    "search.cityList.value":"",
                    "search.cityList.value":"",
                    "search.cityList.value":"",
                    "search.cityList.value":"",
                    "search.cityList.value":"",
                    "search.cityList.value":"",
                    "search.cityList.value":"",
                    "search.cityList.value":"",
                    "search.cityList.value":"",
                    "search.cityList.value":"",
                    "search.cityList.value":"",
                    "search.cityList.value":"",
                    "search.cityList.value":"",
                    "search.cityList.value":"",
                    "search.cityList.value":"",
                    "nowhiringonlystate":"false",
                    "search.stateList.field":"state",
                    "search.stateList.op":"in",
                    "search.cityList.field":"localeLocation.city",
                    "search.cityList.field":"localeLocation.city",
                    "search.cityList.field":"localeLocation.city",
                    "search.cityList.field":"localeLocation.city",
                    "search.cityList.field":"localeLocation.city",
                    "search.cityList.field":"localeLocation.city",
                    "search.cityList.field":"localeLocation.city",
                    "search.cityList.field":"localeLocation.city",
                    "search.cityList.field":"localeLocation.city",
                    "search.cityList.field":"localeLocation.city",
                    "search.cityList.field":"localeLocation.city",
                    "search.cityList.field":"localeLocation.city",
                    "search.cityList.field":"localeLocation.city",
                    "search.cityList.field":"localeLocation.city",
                    "search.cityList.field":"localeLocation.city",
                    "search.cityList.field":"localeLocation.city",
                    "search.cityList.field":"localeLocation.city",
                    "search.cityList.field":"localeLocation.city",
                    "search.cityList.field":"localeLocation.city",
                    "search.cityList.field":"localeLocation.city",
                    "search.cityList.field":"localeLocation.city",
                    "searchObject":"Location",
                    "showResults":"true",
                    "validStructString":"BP9LAIAAAAAAAAAAAAAA%3AF%3AG%3DPEPBDEBBE%3DHFP%3DL%3DPECCDCAAB9N9J%3DG%3BD%3BHGN%40MHFCCEGGL%3BBHEGBFLAI%3BNGNCACGDKHE%3DHHGHA%3CKDL%3DMEM%3DL%3EGAD9JHHCPBODJ%40IBP%40IEHGADMHI%3EGCDDHBD%3BPCE%3AODBDB%3DO%3FM%3AGBPCG%3DGGBDG%3EJ%3EP%3FPHN%3EO%40H%40N%3AI%3FMHODM9GBB%3DB%3FB%3EKAO%3FKCB%3BHCLAJHFDMBC%3CM%3DGHOAJ9JHGBJ%3CBAH9H%3AF%3FH%3ED%40E%40AFHBKFCFLDA9J%3AKENCM%3DEBK%40HDB9PDI%3DM%3AM%40LAM%3BMEH%3DG9ODOHN%3AOHP%40JHFAI%3ECEF%3AI%3BACB%40C9L%3BICJED%3FOECEG%3CGDJBG%3FN%3AA%40KBBHL%40MAE%40E%3AG%3ENBLFH%3DHGJ%3CF%3BHCEGE9EEEBCHLEEEICF%3FGGODD%3FMDIDOGGDE%3FMDL9IDBEK%3AKEI%3ACDAEIECBFAJ%3BGHOBNFB%3FC%3DHAP%3EH%3CGHHHAFDCO%3EM%40L%3ABHN%40HHN%3BO%3AA9G%3DJCNBI%40H9JEA%3ELBE%40L%3FK%3AC%3FD%3ENCO%3FB%40KHC%3BG%3AH%40I%3FADM%3BF%3DK%3CN9L%3DFBGGECDCB9K9EEK%3DMEJ%3EA%40C%3FAAG%40CHN%3BC%3BB9I%3AOAH9I%3FDAJAJFD%3AOEODH%3BHDF%3FEFE%3BKALBOGEDB%3FHCBCP%3BL9K%3BABG%3AGHADFDB%3BACIGI%3FF%3BKFCBDGD%3ALBOAO%3BE%3CCGH%3FKFO%3DCHNEP%3BF%3AGELFC%3DLFNEICN%3DBCOGC9GADFP%3EJ%3DHDBAHEOAK%3AC%3FJ%3BA9IGC%3FF%3EP%3AGDAHLCB9KBLEI%3EM%3DCDM%3CGCAEBGC%3CBAL%40LDA%3FO%3DB%3DMGJ%3FC%3DLDM%3FM%3CCAK%3FKGA%40NGC%3EE9DCLBCHB%3BF%3CGEEHM%3BMGLBEDPFF%3CNHM%40I%3CP%3ACDPEFAC%40P%3CD%3FMCH%3DH%3FC%3FI9A%3AM%3CMEP%3DD%3CAAHGD%3BP%3CE9J%3FLAPACGF%3FC%3ELAL%3ABEH%3CJEO9O%3AP%3FK%3FI%3AN%3CBGKHNDG%3EA%3DB%40EGJEI%3DC%3CM%3DA9IDH%3EL%3DO%3EJFADIDN%3ENDBAJ%3BDACFDBFFH%3FK%3BB9BBE%3ADHA%3BH%3EKBH9DAODIFO%3AI9I%3BOCG%3DOELBNCG%40L%3EF%3DL9O%3EFDPGL%40P%40DFBHK%40P%40HBMFG%40J%3BFDM%3AI%40C%40PDCBBFK%3FLEI%3DE%3FCHDGKDA%3ED%3EH%3FD%3AJ%3CO%3BN%40GDJAJ%3CH%3EGEDCBBF%3BFBAHGADDFAPFIDI%3DP%3BKHJCHFGCE%3AMHCFOCJ%3AKDNFPEBHJ%3DOFBFPAL9N%3EOHO%3CLHJ%40AAFHNBI9C%3AEAL%3DD9C%3CM%3DBBB%3ED%3FJ%3FOAN%3BL%3FD9E%3ABBKBJCMCK9FFI%40A%3FM%3BF%3AB%3AF9CBB%3CJGC9LFMDBCCEL%3CG%3DI%3ACAJ%3CJ%3AM%3CHEECOBLGL%3CJ%3CIGE9JFMFMDCCBBLHFELGE%3BDGOEC%3BOGOFKCCFHDHEN%3DIFK%3DFBCFJ%3BL%3AI%3AA%3FL%3CG%3FNFJDH9P%3CKGN%3FCBFGD%3FCFF%3EL%3EFFDDF%3BOBO%3EH%3CDEE%3CK%3AOAJFJHGCN%3ABGF%3EH9EFM%3CDFN%3AAGL%3DGAFFJ%3CH%3FNHI%3EN%3EIHB%3EHHGCOFN%3FDFMBGGN%3ELFDDE%3CG%3BHGB%3EL%3AO9G%3CBDN9F%3AKCF%3CCFADDCBDHGMFFGO%3CIFB%3DE%3AI%40KCGEP%3ANHN%3CGFP%3DEHPEIBB%40MAB%3EM%40DBF%3DKGFAKAAAA",
                    "SSVCookieName":"SSVCookie_dab4a7cf-5f1e-48d5-8a54-8de93bd7b5f4",
                }
                yield FormRequest(url=url, method="POST", formdata=form_data, headers=headers, callback=self.parse_store)

    def parse_store(self, response):
        try:
            addr = response.xpath("//div[@id='Slot_0_3_3_10_10']/h1/text()").extract_first().strip()
            item = ChainItem()
            item['store_number'] = ""
            item['store_name'] = ""
            item['address'] = addr.split('(')[-1].split(')')[0]
            item['address2'] = ""
            item['city'] = addr.split('(')[0].split(',')[0].strip()
            item['state'] = addr.split('(')[0].split(',')[1].strip()
            item['zip_code'] = ""
            item['latitude'] = ""
            item['longitude'] = ""
            item['country'] = "United States"
            item['phone_number'] = ""
            item['store_hours'] = ""
            item['other_fields'] = ""
            item['coming_soon'] = 0
            yield item
        except:
            pdb.set_trace()
            pass            

    def parse_hour(self, response):
        try:
            item = response.meta['item']
            item['store_hours'] = ""
            class_values = ["time holiday_hours", "time breakfast", "time lunch", "time dinner"]
            for _class_value in class_values:
                class_value = response.xpath('//div[@class="' + _class_value + '"]')
                try:
                    part_hour = class_value.xpath('.//h3/text()').extract_first().strip() + ";"
                except:
                    part_hour = ""
                for hour in class_value.xpath('.//div[@class="hours"]'):
                    value = hour.xpath('.//text()').extract()
                    try:
                        part_hour += value[0].strip() + ":" + value[1].strip() + ";"
                    except:
                        part_hour += ""
                item['store_hours'] += part_hour
                item['phone_number'] = response.xpath('//span[@class="phone"]/text()').extract_first()[1:].strip()
                if '+1' in item['phone_number']:
                    item['country'] = "Mexico"
                elif item['phone_number'].find(')') - item['phone_number'].find('(') == 3:
                    item['country'] = "Brazil"
                else:
                    item['country'] = "United States"
            yield item
        except:
            pass
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
        pos = body.find("var markerData = ") + 18
        stores = "[]"
        store = ""
        while body[pos: pos+2] != "];":
            if body[pos] == "[":
                store = ""
            if body[pos] == "]":
                store += "]"
                stores.append(store)
            store += body[pos]
            pos += 1
        return stores

    def validatePhoneNumber(self, phone_number):
        return phone_number.strip().replace('.', '-')        