import requests
from lxml import html


class Proxy(object):
    proxy_url = 'http://www.ip-adress.com/proxy_list/'
    proxy_list = []

    def __init__(self):
        r = requests.get(self.proxy_url)
        str = html.fromstring(r.content)
        ip = str.xpath("/html/body/main/table/tbody/tr/td[1]/a/text()")
        port = str.xpath("/html/body/main/table/tbody/tr/td[1]/text()")
        result = []
        for i in range(len(ip)):
            result.append('http://'+ ip[i] + port[i])
        self.list = result

    def get_proxy(self):
        proxy_list = self.list
        return proxy_list



def stpr():
    proxy = Proxy()
    proxy = proxy.get_proxy()
    return proxy

stpr()