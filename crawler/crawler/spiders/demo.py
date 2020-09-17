import redis
from crawler import settings
from os import sendfile
import scrapy

from scrapy.utils.project import get_project_settings
from scrapy_redis.spiders import RedisSpider
from scrapy_redis.connection import get_redis_from_settings

# from scrapy_redis.scheduler import enqueue_request
# import ..settings
from ..items import DoubanUrl


# class BaseDistribute(RedisSpider):

#     def start_requests(self):
#         if self.stats.get('is_master', False):



        # def next_request(self):
        #     block_pop_timeout = self.idle_before_close
        #     request = self.queue.pop(block_pop_timeout)
        #     if request and self.stats:
        #         self.stats.inc_value(
        #             'scheduler/dequeued/redis', spider=self.spider)
        # return request



class DemoSpider(scrapy.Spider):
    name = 'demo'
    redis_key = 'demospider:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        # domain = kwargs.pop('domain', '')
        # self.allowed_domains = filter(None, domain.split(','))
        super(DemoSpider, self).__init__(*args, **kwargs)

    # allowed_domains = ['example.com']
    # start_urls = ['http://example.com/']

    def get_export_file_prefix(self):
        return ''

    def start_requests(self):
        url = 'https://book.douban.com/tag/%E7%AE%97%E6%B3%95'

        yield scrapy.Request(
            method='GET',
            url=url,
            headers={},
            callback=self.parse_douban_book,
            meta={}
        )

    def parse_douban_book(self, response):
        url_list = response.xpath('//*[@id="subject_list"]/ul/li/div[2]/h2/a/@href').extract()
        settings = get_project_settings()
        server = get_redis_from_settings(settings)
        for url in url_list[1:6]:
            server.sadd(self.redis_key, url)
        return 

        # for url in url_list:
        #     server.sadd
        #todo Add url to redis
         
            # yield request

            # enqueue_request(request)
            # yield DoubanUrl(
            #     test_url=url
            # )
