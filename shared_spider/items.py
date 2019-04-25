# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class SharedSpiderItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass
class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    publish_time = scrapy.Field()
    content = scrapy.Field()
    type = scrapy.Field()


class StockItem(scrapy.Item):
    code = scrapy.Field()
    abbr = scrapy.Field()
    comment = scrapy.Field()
    price = scrapy.Field()
    rise = scrapy.Field()
    collect_time = scrapy.Field()


class TutorItem(scrapy.Item):
    name = scrapy.Field()
    content = scrapy.Field()
    publish_time = scrapy.Field()
