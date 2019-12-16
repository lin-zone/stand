from stand.db import get_proxy
from stand.utils import add_scheme


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        proxy = get_proxy()
        request.meta['proxy'] = add_scheme(proxy)