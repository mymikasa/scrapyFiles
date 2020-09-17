import redis

import logging
from crawler import settings
from os import sendfile
import scrapy

from scrapy.utils.project import get_project_settings
from scrapy_redis.spiders import RedisSpider
from scrapy_redis.connection import get_redis_from_settings
from scrapy_redis.utils import bytes_to_str

from ..items import DoubanUrl


logger = logging.getLogger(__name__)

class DemoSpider(RedisSpider):
    name = 'demo01'
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

    def next_requests(self):
        server = get_redis_from_settings(self.settings)
        data_raw = server.spop(self.redis_key)
        url = bytes_to_str(data_raw)
        logger.info(url)

        req = scrapy.Request(
            method='GET',
            url=url,
            headers={},
            callback=self.parse_douban_book,
            meta={}
        )
        yield req

    def parse_douban_book(self, response):

        book_url = response.request.url
        book_name = response.xpath('//*[@id="wrapper"]/h1/span').extract_first()
        book_auther = response.xpath('//*[@id="info"]/span[1]/a').extract_first()
        # book_price = response.xpath('//*[@id="info"]/span[1]/a').extract_first()

        yield DoubanUrl(
            book_url=book_url,
            book_name=book_name,
            book_auther=book_auther,
        )

        # url_list = response.xpath(
        #     '//*[@id="subject_list"]/ul/li/div[2]/h2/a/@href').extract()
        # settings = get_project_settings()
        # server = get_redis_from_settings(settings)
        # for url in url_list:
        #     server.sadd(self.redis_key, url)
        # return
