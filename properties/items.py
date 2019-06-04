# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class PropertiesItem(Item):
    title = Field()
    price = Field()

    url = Field()
    server = Field()
    date = Field()


class SchoolItem(Item):
    type = Field()
    name = Field()
    url = Field()

