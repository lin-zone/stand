# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess

from stand._proxies import ProxySpider
from stand.config import CRAWLER_LOG


ITEM_PIPELINES = {
    'stand.utils.SqliteCrawlerPipeline': 300,
}
DOWNLOADER_MIDDLEWARES = {
    'stand.utils.UserAgentMiddleware': 543,
}
settings = dict(
    DOWNLOAD_DELAY=0.5,
    CONCURRENT_REQUESTS=64,
    # LOG_ENABLED=False,
    LOG_LEVEL='INFO',
    LOG_FILE=CRAWLER_LOG,
    RETRY_ENABLED=False,
    DOWNLOAD_TIMEOUT=30,
    ITEM_PIPELINES=ITEM_PIPELINES,
    DOWNLOADER_MIDDLEWARES=DOWNLOADER_MIDDLEWARES,
)


def crawl():
    """爬取代理IP"""
    process = CrawlerProcess(settings=settings)
    process.crawl(ProxySpider)
    process.start()


if __name__ == "__main__":
    crawl()