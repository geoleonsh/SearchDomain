# -*- coding: utf-8 -*-
from openpyxl import Workbook


class SearchdomainPipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['域名', '状态'])

    def process_item(self, item, spider):
        line = [item['domain'], item['state']]
        self.ws.append(line)  # 将数据以行的形式添加到xlsx中
        self.wb.save('顶级域名.xlsx')  # 保存xlsx文件
        return item
