import scrapy

from ..items import DoubanUrl

class ExampleSpider(scrapy.Spider):
    name = 'example'
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

        for url in url_list:
            yield DoubanUrl(
                test_url=url
            )
        
