from stand._base import ProxySpider


class _data5u(ProxySpider):
    start_urls = (
        'http://www.data5u.com/',
    )
    selector = ('css', 'ul.l2')
    ip = ('xpath', '(.//li)[1]/text()')
    port = ('xpath', '(.//li)[2]/text()')


class _66ip(ProxySpider):
    start_urls = (
        'http://www.66ip.cn/{1, 3}.html',
    )
    selector = ('css', 'div#main tr')
    slice = (1, None)
    ip = ('xpath', '(.//td)[1]/text()')
    port = ('xpath', '(.//td)[2]/text()')


class _ip3366(ProxySpider):
    start_urls = (
        'http://www.ip3366.net/free/?stype=1&page={1, 3}',           # 国内高匿
        'http://www.ip3366.net/free/?stype=2&page={1, 3}',           # 国内普通
    )
    selector = ('css', 'div#list tbody tr')
    ip = ('xpath', '(.//td)[1]/text()')
    port = ('xpath', '(.//td)[2]/text()')


# 设置DOWNLOAD_DELAY, 太快会返回503错误
class _kuaidaili(ProxySpider):
    start_urls = (
        'https://www.kuaidaili.com/free/inha/{1, 3}/',
        'https://www.kuaidaili.com/free/intr/{1, 3}/',
        'https://www.kuaidaili.com/ops/proxylist/{1, 3}/',
    )
    selector = ('css', 'div[id$="list"] tbody tr')
    ip = ('xpath', '(.//td)[1]/text()')
    port = ('xpath', '(.//td)[2]/text()')


class _iphai(ProxySpider):
    start_urls = (
        'http://www.iphai.com/',
        'http://www.iphai.com/free/ng',
        'http://www.iphai.com/free/np',
        'http://www.iphai.com/free/wg',
        'http://www.iphai.com/free/wp',
    )
    selector = ('css', 'tr')
    slice = (1, None)
    ip = ('xpath', '(.//td)[1]/text()')
    port = ('xpath', '(.//td)[2]/text()')


class _cz88(ProxySpider):
    start_urls = (
        'http://www.cz88.net/proxy/index.shtml',
        'http://www.cz88.net/proxy/socks4.shtml',
        'http://www.cz88.net/proxy/socks5.shtml',
    )
    selector = ('css', 'div#boxright li')
    slice = (1, None)
    ip = ('css', 'div.ip::text')
    port = ('css', 'div.port::text')


class _freeip(ProxySpider):
    start_urls = (
        'https://www.freeip.top/?page={1, 3}',
    )
    selector = ('css', 'tbody tr')
    ip = ('xpath', '(.//td)[1]/text()')
    port  =('xpath', '(.//td)[2]/text()')


class _proxylistplus(ProxySpider):
    start_urls = (
        'https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-{1, 3}',
        'https://list.proxylistplus.com/Socks-List-{1, 3}',
        'https://list.proxylistplus.com/SSL-List-{1, 3}',
    )
    selector = ('css', 'table.bg tr.cells')
    ip = ('xpath', '(.//td)[2]/text()')
    port = ('xpath', '(.//td)[3]/text()')


class _qydaili(ProxySpider):
    start_urls = (
        'http://www.qydaili.com/free/?action=china&page={1, 3}',
    )
    selector = ('css', 'tbody tr')
    ip = ('xpath', '(.//td)[1]/text()')
    port = ('xpath', '(.//td)[2]/text()')


class _89ip(ProxySpider):
    start_urls = (
        'http://www.89ip.cn/index_{1, 3}.html',
    )
    selector = ('css', 'tbody tr')
    ip = ('xpath', '(.//td)[1]/text()')
    port = ('xpath', '(.//td)[2]/text()')


class _kxdaili(ProxySpider):
    start_urls = (
        'http://www.kxdaili.com/dailiip/1/{1, 3}.html',
        'http://www.kxdaili.com/dailiip/2/{1, 3}.html',
    )
    selector = ('css', 'tbody tr')
    ip = ('xpath', '(.//td)[1]/text()')
    port = ('xpath', '(.//td)[2]/text()')


class _mrhinkydink(ProxySpider):
    start_urls = (
        'http://www.mrhinkydink.com/proxies.htm',
        'http://www.mrhinkydink.com/proxies{2, 16}.htm',
    )
    selector = ('css', 'tr.text')
    slice = (None, -1)
    ip = ('xpath', '(.//td)[1]/text()')
    port = ('xpath', '(.//td)[2]/text()')