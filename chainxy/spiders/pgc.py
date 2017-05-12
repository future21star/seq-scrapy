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

class PgcSpider(scrapy.Spider):
    name = "pgc"
    uid_list = "[]"

    def start_requests(self):
        headers = {
            "Accept":"application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"en-US,en;q=0.8",
            "Connection":"keep-alive",
            "Content-Length":"8584",
            "Content-Type":"application/json",
            "Cookie":"ASP.NET_SessionId=2mr404pok4mv45q51ml0hu0t; _gat=1; _ga=GA1.2.456802075.1494531612; _gid=GA1.2.347775739.1494531614; _gat_nms=1",
            "Host":"www.harnoisgroupepetrolier.com",
            "Origin":"https://www.harnoisgroupepetrolier.com",
            "Referer":"https://www.harnoisgroupepetrolier.com/stations-service",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest",        
        }
        form_data = '{"args":{"FacetsConfiguration":{"Facets":[{"IdentifierGuidType":5,"IsExpandableSection":true,"IsExpandedByDefault":false,"IsMultipleSelection":true,"IsMutuallyExclusive":true,"IsResetSelection":false,"IsRequired":false,"IsCheckBoxSelection":false,"IsProportionalSize":false,"ShowResultCount":true,"IsDropDown":false,"Width":0,"Height":0,"ValueFormat":null,"DropDownWaterMark":null,"DropDownWaterMarkResourceKey":null,"IsVerticalAlignement":true,"HideIfNoResult":false,"CustomText":null,"CustomTextResourceKey":null,"OrderedCustomFieldValueGuids":["4dba8ebb-6348-4ea1-8b4c-9492ba6e2928","6a45c7e2-be43-45a8-aa2c-b0b51d610099","0051b78d-0921-49cb-85a1-5d1860b0dbdc","8c9ba012-e350-4bff-ae93-e47def636e34","19140b01-dc8e-48e6-bfb5-59b7664652d3","f38db91f-c627-4a6e-8879-d54440183b47","3f409c9f-961c-4f23-b60f-a1053a3dca3f","e8979634-a266-4eb8-ad44-f3d397f939ba","5fc61e57-9c61-49ce-9383-6668ad5f11d1","34335cbf-c92d-4e42-9fa7-fa65a46d088a","b3b0fa4a-f49e-4296-ab54-395dc3519b84","b4c67f6c-499d-4344-b4da-b3af29fbaf02","13a3a018-9631-4206-b0ab-0f986067e0bf","51f624e2-07d9-4b56-b264-3d22d0bb7a53","3f7d8a38-f555-49a5-a87f-d8ecc12964f0","62d03315-f0ab-472c-a9c2-c1cf9c2ef0d6","9c5167bc-3f5e-4bdc-8c11-8c7d1d95178d","ad0b2464-8bdc-443e-9962-6fe357cfd976"],"Range":null,"IsDescOrder":false,"ParentTagGuid":"00000000-0000-0000-0000-000000000000","ClassificationGuid":"00000000-0000-0000-0000-000000000000","PropertyName":0,"IdentifierGuid":"e89ae93f-1423-4336-5b91-d68d8b39204b"},{"IdentifierGuidType":5,"IsExpandableSection":true,"IsExpandedByDefault":true,"IsMultipleSelection":true,"IsMutuallyExclusive":true,"IsResetSelection":false,"IsRequired":false,"IsCheckBoxSelection":false,"IsProportionalSize":false,"ShowResultCount":true,"IsDropDown":false,"Width":0,"Height":0,"ValueFormat":null,"DropDownWaterMark":null,"DropDownWaterMarkResourceKey":null,"IsVerticalAlignement":true,"HideIfNoResult":false,"CustomText":null,"CustomTextResourceKey":null,"OrderedCustomFieldValueGuids":["d3c3312f-b522-4c2d-861d-479a5dd861da","6d9f569b-f5b5-4b1d-bd45-4c0bae08e1db","5a2b2844-2561-4d4d-8f74-dd06d76ab5e2"],"Range":null,"IsDescOrder":false,"ParentTagGuid":"00000000-0000-0000-0000-000000000000","ClassificationGuid":"00000000-0000-0000-0000-000000000000","PropertyName":0,"IdentifierGuid":"b5c6c537-ec0a-0904-7a13-1d8f6856d769"},{"IdentifierGuidType":3,"IsExpandableSection":true,"IsExpandedByDefault":true,"IsMultipleSelection":true,"IsMutuallyExclusive":true,"IsResetSelection":false,"IsRequired":false,"IsCheckBoxSelection":false,"IsProportionalSize":false,"ShowResultCount":true,"IsDropDown":false,"Width":0,"Height":0,"ValueFormat":null,"DropDownWaterMark":null,"DropDownWaterMarkResourceKey":null,"IsVerticalAlignement":true,"HideIfNoResult":false,"CustomText":null,"CustomTextResourceKey":null,"OrderedCustomFieldValueGuids":["2d6c28a6-69a4-452f-8c39-f5528f557f02","abc94fc3-0d52-4664-9583-661821c64216","530274a8-bb79-4aef-a8fd-f1c80e6e53c9","3409c4a6-3b4c-4d5e-9723-7eefbc4a79c8","5e6d3b8c-0abf-409e-a767-28ea8b0d6052","7a7e51ae-a456-4ea9-9952-a7ca74d4d8d3","51fd798c-a1ff-4e6a-b3db-467c4cbd71ac","65e824cd-0e44-44b6-80ab-07bf38671b09","9f5a7063-fe9e-4319-b474-1b63be4efc08","d97cce61-ca53-440b-83a5-18e179a45a55","e3995727-45eb-4fef-aea3-4bda9dd50165","4a9f4dac-ac21-4732-acab-456a2439efc4"],"Range":null,"IsDescOrder":false,"ParentTagGuid":"00000000-0000-0000-0000-000000000000","ClassificationGuid":"00000000-0000-0000-0000-000000000000","PropertyName":0,"IdentifierGuid":"5a9cbc82-c069-840e-6468-a756e2fe3cc7"},{"IdentifierGuidType":3,"IsExpandableSection":true,"IsExpandedByDefault":true,"IsMultipleSelection":true,"IsMutuallyExclusive":true,"IsResetSelection":false,"IsRequired":false,"IsCheckBoxSelection":false,"IsProportionalSize":false,"ShowResultCount":true,"IsDropDown":false,"Width":0,"Height":0,"ValueFormat":null,"DropDownWaterMark":null,"DropDownWaterMarkResourceKey":null,"IsVerticalAlignement":true,"HideIfNoResult":false,"CustomText":null,"CustomTextResourceKey":null,"OrderedCustomFieldValueGuids":["8584cae6-b6fd-4878-9be6-6f695ace14b8","e00fe6b0-e743-4496-a685-a1835930abc9","bf7d80a9-db7d-4086-b405-3d829fe3e046","0755abb7-851a-4207-a451-5579c8415170","81ed8f3c-4596-4e5b-aeae-8232aa41211b","d934933c-f87e-4eae-ba75-510f6b43a8e3","31fdb159-8020-4531-aa2f-5dd4039513ee","92e11347-e94f-48e0-a1ad-2a941acb74bc","0a6e6013-b252-4d19-bcc1-0985dc33df44","38901215-c600-47b2-b640-8de9d07bac6c","869f0ccb-b704-41b6-871c-62e1594aa25c"],"Range":null,"IsDescOrder":false,"ParentTagGuid":"00000000-0000-0000-0000-000000000000","ClassificationGuid":"00000000-0000-0000-0000-000000000000","PropertyName":0,"IdentifierGuid":"471813e4-6c89-a38d-6c1e-b4209176cd07"},{"IdentifierGuidType":3,"IsExpandableSection":true,"IsExpandedByDefault":false,"IsMultipleSelection":true,"IsMutuallyExclusive":true,"IsResetSelection":false,"IsRequired":false,"IsCheckBoxSelection":false,"IsProportionalSize":false,"ShowResultCount":true,"IsDropDown":false,"Width":0,"Height":0,"ValueFormat":null,"DropDownWaterMark":null,"DropDownWaterMarkResourceKey":null,"IsVerticalAlignement":true,"HideIfNoResult":false,"CustomText":null,"CustomTextResourceKey":null,"OrderedCustomFieldValueGuids":["faa61d49-f0b5-473c-8364-324d65ed8703","e334aa02-344c-4652-97a7-a1730f0a5172","70085c2f-67b7-4d47-a704-1ecdd48e2d92","17ac30a7-09ad-4599-86fb-3a66c4891cdb","0d914108-48c6-488d-bf72-42334089c746","60fa996b-d0db-4401-85c2-660a018b9068"],"Range":null,"IsDescOrder":false,"ParentTagGuid":"00000000-0000-0000-0000-000000000000","ClassificationGuid":"00000000-0000-0000-0000-000000000000","PropertyName":0,"IdentifierGuid":"58521dc8-62b1-bc80-1976-d4110b6f54d6"},{"IdentifierGuidType":3,"IsExpandableSection":true,"IsExpandedByDefault":false,"IsMultipleSelection":true,"IsMutuallyExclusive":true,"IsResetSelection":false,"IsRequired":false,"IsCheckBoxSelection":false,"IsProportionalSize":false,"ShowResultCount":true,"IsDropDown":false,"Width":0,"Height":0,"ValueFormat":null,"DropDownWaterMark":null,"DropDownWaterMarkResourceKey":null,"IsVerticalAlignement":true,"HideIfNoResult":false,"CustomText":null,"CustomTextResourceKey":null,"OrderedCustomFieldValueGuids":["d71d36a2-4bac-4948-995d-c0e3202d7804","6af5f1fa-10b9-46e7-b04a-304772f520b7","6fce5026-91b3-4965-b6d3-fb3a11bd15d8","319fe2b8-1acf-40dc-83a6-c46ad9242228"],"Range":null,"IsDescOrder":false,"ParentTagGuid":"00000000-0000-0000-0000-000000000000","ClassificationGuid":"00000000-0000-0000-0000-000000000000","PropertyName":0,"IdentifierGuid":"ff5b7261-6219-25d5-2c14-6a648f9bfdc7"},{"IdentifierGuidType":3,"IsExpandableSection":true,"IsExpandedByDefault":false,"IsMultipleSelection":true,"IsMutuallyExclusive":true,"IsResetSelection":false,"IsRequired":false,"IsCheckBoxSelection":false,"IsProportionalSize":false,"ShowResultCount":true,"IsDropDown":false,"Width":0,"Height":0,"ValueFormat":null,"DropDownWaterMark":null,"DropDownWaterMarkResourceKey":null,"IsVerticalAlignement":true,"HideIfNoResult":false,"CustomText":null,"CustomTextResourceKey":null,"OrderedCustomFieldValueGuids":["e56a4673-5a0b-4d45-9c18-7411e2d71f6e","2834154b-b5f4-432b-a3b9-d41b6094020e","99cb26ee-a384-4c67-b564-f74489422e38","309c647f-de88-4883-9833-eb8e0d2bc812","dd95ac53-ab3e-4fd3-9c60-5ea68d82e155","c41bd6e4-e498-46aa-8aa7-41f8348f8228"],"Range":null,"IsDescOrder":false,"ParentTagGuid":"00000000-0000-0000-0000-000000000000","ClassificationGuid":"00000000-0000-0000-0000-000000000000","PropertyName":0,"IdentifierGuid":"bd2fb959-a97c-5e49-be45-cbdb15f2e762"}],"Tags":["6f6e5504-b7c4-d532-c590-a45ce7fabdb1"],"CatalogGuid":"00000000-0000-0000-0000-000000000000","RedirectionZoneHierarchyId":0,"GroupByFamily":false,"GroupingCustomFieldGuids":[],"GetOnlyProductsWithUrl":true,"IsRedirectOnSelect":true,"HasGroupedQueryZone":false},"CustomFieldGuids":["0ddfe0bd-f24d-2bb3-11a1-a229c230d7cc","fd9da13c-90ff-352a-ba8b-b2be00151fa8","75d2f032-6a23-2460-029d-6c23a12f663d","4d135442-0343-74a2-c734-0eb160c152d0","47e5383a-a0a3-2edf-4efc-04449dd7652b","a711d5fe-3dd0-e3ce-111f-107160ab0735","e700ac5e-c123-837b-f6e7-ec1558a92d31","26e9ad4d-1943-ba33-eb46-580daed3f77a","8edcef11-5956-5560-4d58-b63231bab883","b827d3c3-8ed9-0bfc-0ddd-7ad113c22799","207ad1e6-ed61-c43e-58fe-a3600aa5e5c2","bce0cbba-0245-900a-d0b7-453a70a2ae87","6e26687e-ce19-6439-30d4-1fb63110bf3c","a839c827-a5ad-025e-04ec-b3a76c4dc400","dffb8404-89ad-29a6-5e4f-efa43db48e69","6f72bf1f-a7d0-f372-0e00-622737794ed7","9d5a5217-fa1e-2de6-71c6-a54b15032e2e","54937d36-658f-4621-9474-8f292aa57a1a"],"CultureId":"fr-CA","CurrencyId":1,"Facets":[],"Search":"","OrderBy":null,"IsDescOrder":true,"Index":0,"Count":400}}'
        url = "https://www.harnoisgroupepetrolier.com/Service/InventoryService.asmx/GetProductsByFacets?fr-CA8682cc0e-ccf8-4604-a733-b18f0ca7c0c7"
        yield  scrapy.Request(url=url, method="POST", body=form_data, headers=headers, callback=self.parse_store)

    def parse_store(self, response):
        try:
            stores = json.loads(response.body)["d"]["Products"]
            for store in stores:
                item = ChainItem()
                item['store_number'] = store["ProductId"]
                item['store_name'] = store["Name"]
                item['address'] = store["CustomFieldValues"][1]["Value"].split("<br>")[0]
                item['address2'] = ""
                item['city'] = store["CustomFieldValues"][1]["Value"].split("<br>")[1].split(',')[0]
                item['state'] = store["CustomFieldValues"][1]["Value"].split("<br>")[1].split(',')[1]
                item['zip_code'] = store["CustomFieldValues"][1]["Value"].split("<br>")[2]
                item['latitude'] = store["CustomFieldValues"][2]["Value"]
                item['longitude'] = store["CustomFieldValues"][3]["Value"]
                item['country'] = "Canada"
                item['phone_number'] = store["CustomFieldValues"][5]["Value"]
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