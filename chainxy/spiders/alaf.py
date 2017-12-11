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
import yaml

class AlafSpider(scrapy.Spider):
		name = "alaf"
		uid_list = []
		start_urls = ['http://www.alafarm.com/locations/storelist/default.aspx']

		def parse(self, response):
			for store in response.xpath("//tr[contains(@class, 'grdRow')]"):					
				if len(store.xpath('./td')) > 0:
					item = ChainItem()
					item['store_number'] = ""
					item['store_number1'] = ""
					item['store_number2'] = ""
					item['store_name'] = self.validate(store.xpath('./td[1]/a[1]/text()'))
					item['address'] = self.validate(store.xpath('./td[2]/span[1]/text()'))
					item['address2'] = ""
					item['city'] = store.xpath('./td[2]/span[1]/text()').extract()[1].split(',')[0].strip()
					item['state'] = store.xpath('./td[2]/span[1]/text()').extract()[1].split(',')[1].split()[0].strip()
					item['zip_code'] = " ".join(store.xpath('./td[2]/span[1]/text()').extract()[1].split(',')[1].split()[1:]).strip()
					item['country'] = "United States" 
					item['phone_number'] = self.validate(store.xpath('./td[3]/span[1]/text()'))
					item['store_hours'] = ""
					lat_lng = self.validate(store.xpath('.//a[contains(@href, 	"http://maps.google.com/maps?")]/@href'))
					if lat_lng != "":
						item['latitude'] = lat_lng.split('ll=')[1].split(',')[0]
						item['longitude'] = lat_lng.split('ll=')[1].split(',')[1].split('&')[0]
					else:
						item['latitude'] = ""
						item['longitude'] = ""
					#item['store_type'] = info_json["@type"]
					item['other_fields'] = ""
					item['coming_soon'] = 0
					yield item		

		def parse_hour(self, response):
			try:
				store = yaml.load(response.body.split("var locationList = '")[-1].split('},]}')[0] + '},]}')['locationData'][0]
				item = response.meta['item']
				item['store_hours'] = store['LobbyHour']
				yield item
			except:
				pdb.set_trace()
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
				# 	pdb.set_trace()
				return formatted_value
			except:
				return source
		def format(self, item):
			try:
				return unicodedata.normalize('NFKD', item).encode('ascii','ignore').strip()
			except:
				return ''			




import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AlertService, AdminService } from '../../../_services/index';

@Component({
    templateUrl: 'new_company.component.html',
    styleUrls: ['new_company.component.scss']
})

export class NewCompanyComponent implements OnInit{
    private model: any = {};
    private loading = false;
    private company_emails: String[] = [];
    
    constructor(
        private router: Router,
        private adminService: AdminService,
        private alertService: AlertService) { }

    ngOnInit() {
      this.getEmails();
    }
    
    register() {
        if (this.company_emails.indexOf(this.model.email) === -1) {
            this.loading = true;
            this.adminService.addCompany(this.model)
                .subscribe(
                    data => {
                        this.alertService.success('Successfully added', true);
                        this.adminService.sendInvitationToCompany(data)
                        .subscribe(
                            data => {
                                this.router.navigate(['/admin/manage_company']);
                            },
                            error => {
    
                            }
                        );
                    },
                    error => {
                        console.log("service error");
                        this.alertService.error(error);
                        this.loading = false;
                    });
        }
    }
    
    getEmails() {
      this.adminService.getCompanies().subscribe(
        data => {
            for (let index in data) {
                this.company_emails.push(data[index].email);
            }
            console.log(this.company_emails);
        },
        error => console.log(error),
        () => {this.loading = false}
      );
    }
}
