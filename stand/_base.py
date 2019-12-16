import re

import scrapy
from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Compose

from stand.utils import gen_urls, get_domain


class ProxyItem(Item):
    ip = Field()
    port = Field()


class ProxyLoader(ItemLoader):
    default_item_class = ProxyItem
    default_output_processor = Compose(TakeFirst(), str.strip)


class ProxySpider(scrapy.Spider):
    name = 'proxy'

    def start_requests(self):
        self.logger.info("start crawl proxy")
        for proxy_cls in self.all_proxies():
            proxy = proxy_cls()
            for url in proxy.get_urls():
                yield scrapy.Request(url, callback=proxy.parse, errback=proxy.err_parse)

    def get_urls(self):
        for url in self.start_urls:
            yield from gen_urls(url)

    def parse(self, response):
        selectors = getattr(response, self.selector[0])(self.selector[1])
        if hasattr(self, 'slice'):
            selectors = selectors[slice(*self.slice)]
        for selector in selectors:
            l = ProxyLoader(selector=selector)
            for field in ProxyItem.fields:
                if hasattr(self, field):
                    values = getattr(self, field)
                    getattr(l, 'add_{}'.format(values[0]))(field, values[1])
            item = l.load_item()
            print(f"{item['ip']}:{item['port']}")
            yield item

    def err_parse(self, failure):
        domain = get_domain(failure.request.url)
        msg = f"{domain} {failure.value}"
        print(msg)
        self.logger.info(msg)

    def all_proxies(self):
        cls = self.__class__
        return cls.__subclasses__() or [cls]
