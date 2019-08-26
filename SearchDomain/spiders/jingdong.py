# -*- coding: utf-8 -*-
import random
import string
import urllib.parse
import scrapy
from scrapy.spiders import Request
from items import SearchdomainItem


class JingdongSpider(scrapy.Spider):
    name = "searchdomain"
    allowed_domains = ["net.jdcloud.com"]
    api_url = 'https://net.jdcloud.com/search/searchDomain?'
    # 修改域名后缀
    suffix = '.com'
    # 修改域名字母个数
    count = 5

    def start_requests(self):
        low_case = string.ascii_lowercase
        product_name = self.suffix
        # 注意为了简便采用了随机算法而不是遍历算法，调用26**4次必定没有完全遍历4个字母组合的所有可能，可适当增加次数
        for i in range(26 ** 4):
            domain_name = ''.join(random.sample(low_case, self.count))
            param = {'domainName': domain_name, 'productName': product_name}
            url = self.api_url + urllib.parse.urlencode(param)
            yield Request(url, callback=self.page_parse)

    def page_parse(self, response):
        sel = scrapy.Selector(response)
        domain = sel.xpath('//table[@class="search-tbl"]/tbody/tr[1]/td/text()').extract_first()
        state = sel.xpath('//table[@class="search-tbl"]/tbody/tr[1]/td/span/text()').extract_first()
        item = SearchdomainItem()
        item['domain'] = domain
        item['state'] = state
        return item
