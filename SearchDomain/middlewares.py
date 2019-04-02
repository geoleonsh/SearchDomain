# -*- coding: utf-8 -*-

from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import DesiredCapabilities


class SearchdomainSpiderMiddleware(object):
    def process_request(self, request, spider):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        SERVICE_ARGS = ['--disk-cache=true', '--ignore-ssl-errors=true']
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201")
        driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=SERVICE_ARGS)
        driver.start_session(dcap)
        driver.set_page_load_timeout(20)
        try:
            driver.get(request.url)
        except TimeoutException as e:
            print(e)
            driver.execute_script('window.stop()')
        return HtmlResponse(url=driver.current_url, body=driver.page_source, encoding='utf-8',
                            request=request)
