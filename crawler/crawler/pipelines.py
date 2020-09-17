# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface\
import logging
import os
from datetime import datetime
from itemadapter import ItemAdapter
from os import path

from scrapy import signals
from scrapy.exporters import JsonLinesItemExporter

from crawler.libs.env import JOB_ID
from .items import (
    DoubanUrl,
)

logger = logging.getLogger(__name__)

class BasePipeline:
    def process_item(self, item, spider):
        if isinstance(item, DoubanUrl):
            item = self.process_raw_douban_url_item(item, spider)
        return item


    def process_raw_douban_url_item(item, spider):
        return item
        

class JsonlineExporter(JsonLinesItemExporter):

    def finish_exporting(self):
        self.file.close()


class JSONFileExporterPipeline(BasePipeline):
    """
    将爬取结果固化到文件
    """

    def __init__(self):
        super(JSONFileExporterPipeline, self).__init__()
        self.exporters = {}
        self.exporters_file = {}
        self.registered = False

    @staticmethod
    def get_export_sub_dir(spider):
        return "{}_{}".format(spider.name, str(JOB_ID))

    @staticmethod
    def get_export_file(item_type):
        date = datetime.now().strftime('%Y%m%d')
        return f'{JOB_ID}_{date}_{item_type}.json'
    
    def register_signal(self, crawler):
        if self.registered:
            return
        self.registered = True
        crawler.signals.connect(
            self.on_spider_closed, signal=signals.spider_closed
        )

    def on_spider_closed(self, spider, reason):
        for f, exporter in self.exporters_file.items():
            exporter.finish_exporting()

        if not spider.crawler.settings.get('UPLOAD_TO_OSS'):
            for f, exporter in self.exporters_file.items():
                exporter.finish_exporting()
            return

        # Async import crawler data for market spiders
        if hasattr(spider, 'job_recorder') and reason == 'finished':
            spider.job_recorder.add(JOB_ID)

    def get_exporter(self, item, spider):
        item_type = item.__class__.__name__
        output_dir = spider.crawler.settings.get('OUTPUT_DIR')
        output_dir = path.join(
            output_dir,
            spider.get_export_file_prefix(),
            self.get_export_sub_dir(spider)
        )
        if not path.exists(output_dir):
            os.makedirs(output_dir)
        if item_type not in self.exporters:
            file_path = path.join(
                output_dir, self.get_export_file(item_type))
            exporter = JsonlineExporter(open(file_path, 'wb'))
            exporter.start_exporting()
            self.exporters[item_type] = exporter
            self.exporters_file[file_path] = exporter
            if not self.registered:
                self.register_signal(spider.crawler)
        return self.exporters[item_type]

    def process_item(self, item, spider):
        if spider.crawler.settings.get('EXPORT_JSON'):
            exporter = self.get_exporter(item, spider)
            exporter.export_item(item)
        return item
