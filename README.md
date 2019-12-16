# IP 代理池

## 安装

```sh
pip install stand
```

## 启动

```sh
stand
```

## 使用

```python
>>> from stand import get_proxy
>>> proxy = get_proxy()
>>> print(proxy)
'103.133.222.151:8080'
```

在 Scrapy 中使用 stand 作为代理

```python
import scrapy
from scrapy.crawler import CrawlerProcess


class TestSpider(scrapy.Spider):
    name = 'test'
    start_urls = ['https://api.ip.sb/ip']

    def parse(self, response):
        print(response.meta['proxy'])
        print(response.text)


DOWNLOADER_MIDDLEWARES = {
    'stand.UserAgentMiddleware': 543,
    'stand.ProxyMiddleware': 600,
}
settings = dict(
    LOG_ENABLED=False,
    DOWNLOAD_TIMEOUT=30,
    DOWNLOADER_MIDDLEWARES=DOWNLOADER_MIDDLEWARES,
)


def run():
    process = CrawlerProcess(settings)
    process.crawl(TestSpider)
    process.start()


if __name__ == "__main__":
    run()
```

## 项目说明

1. 当启动 `stand` 时, 首先会运行 `crawl` 函数从代理网站爬取代理 IP, 并将爬取到的结果存储在名为 stand.db (可通过 `STAND_DB` 环境变量设置路径) 的 SQLite 数据库中, 每个 IP 有一个初始分数 2
2. 然后会运行 `validate` 函数验证代理 IP 的有效性, 验证通过分数设置为最高值 3, 验证失败分数减 1, 当分数为 0 时删除该 IP
3. 之后会定时运行 `crawl` 和 `validate` 函数分别爬取和验证 IP, 每20分钟爬取一次 IP, 每60分钟验证一次 IP
