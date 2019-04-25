# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from shared_spider.items import ArticleItem, StockItem, TutorItem


class SharedSpiderPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456',
                                    db='shared', charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item, ArticleItem):
            try:
                sql = '''insert into article(title, content, publish_time, type) values(%s, %s, %s, %s)'''
                param = (item['title'], item['content'], item['publish_time'], item['type'])
                self.cursor.execute(sql, param)
                self.conn.commit()
            except Exception as e:
                print('插入article表失败' + str(e))
        elif isinstance(item, StockItem):
            try:
                sql = '''insert into comment(code, abbr, comment, price, rise, collect_time) 
                         values(%s, %s, %s, %s, %s, %s)'''
                param = (item['code'], item['abbr'], item['comment'], item['price'], item['rise'], item['collect_time'])
                self.cursor.execute(sql, param)
                self.conn.commit()
            except Exception as e:
                print('插入comment表失败' + str(e))
        elif isinstance(item, TutorItem):
            try:
                sql = '''insert into tutor(name, content, publish_time) 
                         values(%s, %s, %s)'''
                param = (item['name'], item['content'], item['publish_time'])
                self.cursor.execute(sql, param)
                self.conn.commit()
            except Exception as e:
                print('插入tutor表失败' + str(e))
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
