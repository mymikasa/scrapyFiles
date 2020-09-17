from ..libs.ua.ua import get_user_agent


class FakeUAMiddleware(object):

    def __init__(self, spider):
        super(FakeUAMiddleware, self).__init__()
        self.spider = spider

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.spider)

    def process_request(self, request, spider):
        if request.headers.get('User-Agent', None) is None:
            request.headers['User-Agent'] = get_user_agent()