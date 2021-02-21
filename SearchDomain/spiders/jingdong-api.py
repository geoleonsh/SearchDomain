# -*- coding: utf-8 -*-
import string
import scrapy
import json
from scrapy import FormRequest
from items import SearchdomainItem


class APISpider(scrapy.Spider):
    name = "searchdomain2"
    allowed_domains = ["net.jdcloud.com"]
    api_url = 'https://net.jdcloud.com/search/getDomainPriceAndRegisterState'
    # 修改域名后缀
    suffix = '.net'

    def start_requests(self):
        list1 = string.ascii_lowercase
        list2 = 'aoeiuv'
        for i in list1:
            for j in list2:
                for k in list1:
                    for l in list2:
                        domain = ''.join([i, j, k, l])
                        param_data = {"productName": self.suffix, "domainName": domain, "searchIndex": '0'}
                        yield FormRequest(url=self.api_url, callback=self.page_parse, method='POST',
                                          formdata=param_data)

    def page_parse(self, response):
        recieved_data = response.body.decode()
        json_data = json.loads(recieved_data)
        key = json_data['domainName']
        state = json_data['flag']
        item = SearchdomainItem()
        item['domain'] = key
        item['state'] = state
        return item
