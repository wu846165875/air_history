# -*- coding: utf-8 -*-
import scrapy
from air_history.items import AirHistoryItem


class AirSpiderSpider(scrapy.Spider):
    name = 'air_spider'
    allowed_domains = ['aqistudy.cn']
    base_url = 'https://www.aqistudy.cn/historydata/'
    start_urls = [base_url]

    def parse(self, response):
        # 提取城市链接
        city_link_list = response.xpath('//ul[@class="unstyled"]/li/a/@href').extract()

        # 提取城市名称
        city_name_list = response.xpath('//ul[@class="unstyled"]/li/a/text()').extract()

        for name, link in zip(city_name_list[0:1], city_link_list[0:1]):
            url = self.base_url + link
            yield scrapy.Request(url=url, callback=self.parse_month, meta={'city': name})

    # 解析月份信息
    def parse_month(self, response):
        # 获取月份链接
        url_list = response.xpath('//table/tbody/tr/td/a/@href').extract()

        for url in url_list:
            url = self.base_url + url
            yield scrapy.Request(url=url, callback=self.parse_day, meta={'city': response.meta['city']})

    # 获取每一天的信息
    def parse_day(self, response):
        # 获取每一天的空气情况
        node_list = response.xpath('//table/tbody/tr')
        # 取出标题行
        node_list.pop(0)
        for node in node_list:
            item = AirHistoryItem()
            item['data'] = node.xpath('./td[1]/text()').extract_first()
            item['city'] = response.meta['city']
            item['aqi'] = node.xpath('./td[2]/text()').extract_first()
            item['level'] = node.xpath('./td[3]/text()').extract_first()
            item['pm2_5'] = node.xpath('./td[4]/text()').extract_first()
            item['pm10'] = node.xpath('./td[5]/text()').extract_first()
            item['so2'] = node.xpath('./td[6]/text()').extract_first()
            item['co'] = node.xpath('./td[7]/text()').extract_first()
            item['no2'] = node.xpath('./td[8]/text()').extract_first()
            item['o3'] = node.xpath('./td[9]/text()').extract_first()
            yield item
