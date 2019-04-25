import scrapy
import datetime
from shared_spider.items import TutorItem
from scrapy_redis.spiders import RedisSpider


class Tutor(RedisSpider):
    name = 'tutor_spider'
    redis_key = 'tt:start_urls'
    # start_urls = ['http://live.gushidaoshi.com/']

    def parse(self, response):
        tutors = response.xpath('//div[@class="ds_lists"]/a')
        for tutor in tutors:
            if tutor.xpath('@class').extract_first() == 'nolive':
                continue
            url = tutor.xpath('@href').extract_first()
            yield scrapy.Request(url=url, callback=self.parse_content)

    def parse_content(self, response):
        item = TutorItem()
        name = response.xpath('//*[@id="headImg"]/tbody/tr/td[1]/span/text()').extract_first()
        print(name)
        item['name'] = name
        dt = datetime.datetime.now().strftime("%Y-%m-%d")
        views = response.xpath('//div[@id="msgDiv"]/dl/dd')
        for view in views:
            time = view.xpath('p/span/text()').extract_first()
            time = dt + ' ' + time + ':00'
            time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
            print(time)
            item['publish_time'] = time
            content = view.xpath('div').xpath('string(.)').extract_first()
            if content:
                content = content.strip()
            else:
                content = ''
            print(content)
            item['content'] = content
            yield item
