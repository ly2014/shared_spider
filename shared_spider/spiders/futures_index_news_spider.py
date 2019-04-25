import scrapy
import datetime
from shared_spider.items import ArticleItem
from scrapy_redis.spiders import RedisSpider


class FuturesIndexNews(RedisSpider):
    name = 'fin_spider'
    redis_key = 'fin:start_urls'
    # start_urls = ['http://if.stockstar.com/list/3191.shtml']

    def parse(self, response):
        news = response.xpath('//ul[@class="list-line"]/li')
        now = datetime.datetime.now()
        for new in news:
            dt = new.xpath('span/text()').extract_first()
            if not dt:
                continue
            dt = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
            if ((now.year - dt.year) * 12 + now.month - dt.month) > 2:
                return
            item = ArticleItem()
            title = new.xpath('a/text()').extract_first()
            item['title'] = title
            item['publish_time'] = dt
            item['type'] = 16
            item['content'] = ''
            url = new.xpath('a/@href').extract_first()
            yield scrapy.Request(url=url, callback=self.parse_content, meta={'item': item})
        next_page = response.xpath('//div[@id="Page"]/span[2]/a/@href').extract_first()
        if next_page:
            url = 'http://if.stockstar.com/list/' + next_page
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_content(self, response):
        item = response.meta['item']
        content = item['content']
        tr = response.xpath('//div[@id="container-article"]//table//tr')
        for r in tr:
            content += r.xpath('string(.)').extract_first()
        ps = response.xpath('//div[@id="container-article"]/p')
        for p in ps:
            if p.xpath('select').extract_first():
                continue
            if p.xpath('@class').extract_first() == 'noIndent':
                continue
            content += p.xpath('string(.)').extract_first()
        item['content'] = content
        next_page = response.xpath('//div[@id="Page"]/span[2]/a/@href').extract_first()
        if next_page:
            url = 'https://stock.stockstar.com/' + next_page
            yield scrapy.Request(url=url, callback=self.parse_content, meta={'item': item})
        else:
            yield (item)