# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime


class BaseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    scraped_time = scrapy.Field()

    def __init__(self, *args, **kwds):
        super(BaseItem, self).__init__(*args, **kwds)
        if 'scraped_time' not in kwds:
            self['scraped_time'] = datetime.datetime.now().strftime(
                self.DATETIME_FORMAT
            )

    @property
    def scraped_time_obj(self):
        return datetime.datetime.strptime(
            self['scraped_time'], self.DATETIME_FORMAT
        )


class DoubanUrl(BaseItem):
    test_url = scrapy.Field()



