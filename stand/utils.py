import re

from fake_useragent import UserAgent

from stand.db import SqliteDB


_proxy_re = r'^\d+.\d+.\d+.\d+:\d+$'
_ip_re = r'^\d+.\d+.\d+.\d+$'
_url_range_re = r'{(\d+),\s*(\d+)}'


def is_proxy(proxy):
    """判断是否有效代理
    >>> is_proxy('127.0.0.1:80')
    True
    >>> is_proxy('a12.df.qe.3:1')
    False
    """
    return bool(re.match(_proxy_re, proxy))


def is_ip(ip):
    """判断是否有效IP
    >>> is_ip('127.0.0.1')
    True
    >>> is_ip('a12.df.qe.3')
    False
    """
    return bool(re.match(_ip_re, ip))


def add_scheme(proxy, https=True):
    scheme = 'https' if https else 'http'
    return f'{scheme}://{proxy}'


def remove_scheme(proxy, https=True):
    scheme = 'https' if https else 'http'
    return proxy.strip(f'{scheme}://')


def gen_urls(url):
    """根据输入的url字符串产生一个url生成器
    >>> urls = gen_urls('http://www.data5u.com/')
    >>> next(urls)
    'http://www.data5u.com/'
    >>> next(urls)
    StopIteration
    >>> urls = gen_urls('http://www.66ip.cn/{1, 2}.html')
    >>> next(urls)
    'http://www.66ip.cn/1.html'
    >>> next(urls)
    'http://www.66ip.cn/2.html'
    >>> next(urls)
    StopIteration
    """
    m = re.search(_url_range_re, url)
    if m:
        start, stop = map(int, m.groups())
        fmt_url = re.sub(_url_range_re, '{}', url)
        for offset in range(start, stop + 1):
            yield fmt_url.format(offset)
    else:
        yield url


class SqliteCrawlerPipeline(object):

    def open_spider(self, spider):
        self._db = SqliteDB()

    def process_item(self, item, spider):
        proxy = f"{item['ip']}:{item['port']}"
        if is_proxy(proxy):
            self._db.add(proxy)
        return item

    def close_spider(self, spider):
        self._db.clean()
        self._db.close()


class SqliteValidatorPipeline(object):

    def open_spider(self, spider):
        self._db = SqliteDB()
        spider.proxies = self._db.all()

    def process_item(self, item, spider):
        status, proxy = item['status'], item['proxy']
        if status:
            self._db.max_score(proxy)
        else:
            self._db.decrease_score(proxy)
        return item

    def close_spider(self, spider):
        self._db.clean()
        self._db.close()


class UserAgentMiddleware(object):
    ua = UserAgent()

    def process_request(self, request, spider):
        request.headers['User-Agent'] = self.ua.random