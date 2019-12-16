# -*- coding: utf-8 -*-
import os

import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.crawler import CrawlerProcess

from stand.utils import is_ip, add_scheme, remove_scheme


class ValidatorSpider(scrapy.Spider):
    name = 'validator'
    api_url = 'https://api.ip.sb/ip'

    def get_request(self, proxy=None, **kwargs):
        meta = {}
        if proxy is not None:
            meta['proxy'] = add_scheme(proxy)
        return scrapy.Request(self.api_url, meta=meta, dont_filter=True, **kwargs)

    def start_requests(self):
        self.logger.info("start validate proxy")
        yield self.get_request(callback=self.parse)

    def parse(self, response):
        ip = response.text
        if is_ip(ip):
            self.local_ip = ip
        else:
            raise CloseSpider("本地IP获取失败")
        for proxy in self.proxies:
            yield self.get_request(
                proxy=proxy,
                callback=self.parse_proxy,
                errback=self.error_parse,
            )

    def parse_proxy(self, response):
        ip = response.text
        if not is_ip(ip):                       # 无效ip, 跳过
            return
        status = ip != self.local_ip            # 验证IP是否等于本地IP
        proxy = remove_scheme(response.meta['proxy'])
        print(f"{proxy} validate {status}")
        yield dict(proxy=proxy, status=status)

    def error_parse(self, failure):
        proxy = remove_scheme(failure.request.meta['proxy'])
        print(f"{proxy} validate False")
        yield dict(proxy=proxy, status=False)


ITEM_PIPELINES = {
    'stand.utils.SqliteValidatorPipeline': 300,
}
DOWNLOADER_MIDDLEWARES = {
    'stand.utils.UserAgentMiddleware': 543,
}
settings = dict(
    DOWNLOAD_DELAY=0.1,
    CONCURRENT_REQUESTS=100,
    # LOG_ENABLED=False,
    LOG_LEVEL='INFO',
    LOG_FILE=os.environ.get('VALIDATOR_LOG', './validator.log'),
    RETRY_ENABLED=False,
    DOWNLOAD_TIMEOUT=15,
    ITEM_PIPELINES=ITEM_PIPELINES,
    DOWNLOADER_MIDDLEWARES=DOWNLOADER_MIDDLEWARES,
)


def validate():
    process = CrawlerProcess(settings=settings)
    process.crawl(ValidatorSpider)
    process.start()   


if __name__ == "__main__":
    validate()