# -*- coding: utf-8 -*-

from urllib import parse

import scrapy


class SchoolSpider(scrapy.Spider):
    name = 'school'

    def start_requests(self):
        base = 'http://nj.sell.house365.com/school/sl_c2.html'
        yield scrapy.Request(url=base, callback=self.parse)
        for i in range(2, 31):
            yield scrapy.Request(url=parse.urljoin(base, 'sl_c2-p%s.html' % i), callback=self.parse)


    def parse(self, response):
        for component in response.css('.clearfix.xq_fl'):
            image = component.css('.else_info.xq_lh2.imgbot')[0]
            yield {
                'name': component.css('.schooltitle::text')[0].get(),
                'district': component.css('.infodd.else_info')[0].css('span.txt::text').get(),
                'level': image.css('.txtname::text')[1].get(),
                'public': image.css('.txtname::text')[2].get(),
                'communityLink': component.css('.xqtxt::attr(href)')[1].get()
            }

