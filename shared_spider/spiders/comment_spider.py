import scrapy
import datetime
from shared_spider.items import StockItem
from scrapy_redis.spiders import RedisSpider


class Comment(RedisSpider):
    name = 'comment_spider'
    redis_key = 'ct:start_urls'
    # start_urls = ['http://quote.stockstar.com/Comment/5_1_1.html']
    page = 1
    dt = datetime.datetime.now()

    def parse(self, response):
        body = response.xpath('//tbody[@id="t_body"]/tr')
        if len(body) > 1:
            self.page += 1
            url = 'http://quote.stockstar.com/Comment/5_1_%s.html' % self.page
            yield scrapy.Request(url=url, callback=self.parse)
            for tr in body:
                item = StockItem()
                code = tr.xpath('td[2]/text()').extract_first()
                print(code)
                item['code'] = code
                abbr = tr.xpath('td[3]/a/text()').extract_first()
                print(abbr)
                item['abbr'] = abbr
                comment = tr.xpath('td[4]/text()').extract_first()
                print(comment)
                item['comment'] = comment
                price = tr.xpath('td[5]/span/text()').extract_first()
                print(price)
                item['price'] = price
                rise = tr.xpath('td[6]/span/text()').extract_first()
                print(rise)
                item['rise'] = rise
                item['collect_time'] = self.dt
                yield item

