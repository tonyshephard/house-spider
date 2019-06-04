# -*- coding: utf-8 -*-

from urllib import parse

import scrapy
import csv


class CommunitySpider(scrapy.Spider):
    name = 'community'

    def start_requests(self):
        school_reader = csv.reader(open('school-test.csv', newline=''), delimiter=',', quotechar='|')
        counter = 0
        name_index, link_index, level_index= 0 , 0, 0
        for row in school_reader:
            counter = counter + 1
            if counter > 1:
                yield scrapy.Request(url=row[link_index], callback=self.parse, meta={
                    'school-name': row[name_index],
                    'school-level': row[level_index]
                })
            else:
                name_index = row.index('name')
                level_index = row.index('level')
                link_index = row.index('communityLink')

    def parse(self, response):
        for link in response.css('.pagination')[0].css('a::attr(href)').getall():
            yield scrapy.Request(url=link, callback=self.parse_community, meta=response.meta)

    def parse_community(self, response):
        for name in response.css('.mask::text').getall():
            # link in beike, filter condition: near MRT, 60-110m^2
            link_ke = 'https://nj.ke.com/ershoufang/su1a2a3bp0ep500rs%s/' % name
            yield scrapy.Request(url=link_ke, callback=self.parse_house, meta=response.meta)

    def parse_house(self, response):
        if response.xpath('//div[contains(@id, "noResultIds")]'):
            pass
        for item in response.css('.sellListContent')[0].css('.clear'):
            yield {
                'schoolName': response.meta.get('school-name'),
                'schoolLevel': response.meta.get('school-level'),
                'community': item.css('.positionInfo')[0].css('a::text').get(),
                'totalPrice': item.css('.totalPrice span::text').get(),
                'unitPrice': item.css('.unitPrice span::text').get(),
                'houseInfo': ' '.join(item.css('.houseInfo::text')[1].get().split()),
                'note': item.css('.title a::text').get(),
                'link': item.css('.title a::attr(href)').get()
            }
