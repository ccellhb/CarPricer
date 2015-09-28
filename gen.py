#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# RH CREATED 20150801

import urllib.request, asyncio ,aiohttp
from doxls import write_excel   
import time
from html.parser import HTMLParser
from util import getProxyConfig

# define query list
query_list = [
              {'make': 'toyota', 'mode': 'venza'},
              {'make': 'toyota', 'mode': 'rav4'},
              {'make': 'toyota', 'mode': 'highlander'},
              {'make': 'ford', 'mode': 'escape'},
              {'make': 'ford', 'mode': 'edge'},
              {'make': 'lexus', 'mode': 'nx%20200t'}
              ]


global list_result
list_result = []


class MyParser(HTMLParser):

    global list_result

    def __init__(self, make, mode):
        super(MyParser, self).__init__()
        self._flag = ''

        self._name_list = []
        self._price_list = []
        self._url_list = []
        self._pic_list = []
        self._make = make
        self._mode = mode

    def handle_starttag(self, tag, attrs):
        if ('class', 'resultTitle') in attrs:
            self._flag = 'Name:'
        elif ('itemprop', 'price') in attrs:
            self._flag = 'Price:'
        elif ('itemprop', 'url') in attrs and attrs[0][1] != "url":
            self._url_list.append(attrs[0][1])

    def handle_endtag(self, tag):
        pass

    def handle_startendtag(self, tag, attrs):
        if tag == 'img':
            if ('width','96') in attrs:
                self._pic_list.append(attrs[3][1])

    def handle_comment(self, data):
        pass

    def handle_entityref(self, name):
        pass

    def handle_charref(self, name):
        pass

    def error(self, message):
        pass

    def handle_data(self, data):
        if data.strip() is not '':
            if self._flag == 'Name:':
                self._name_list.append(data.strip())
            elif self._flag == 'Price:':
                self._price_list.append(data.strip())

            self._flag = ''

    def merge(self):
        i = 0
        while i < len(self._name_list):
            dict_carinfo = {'make': self._make, 'mode': self._mode, 'name': self._name_list[i],
                            'price': self._price_list[i], 'url': self._url_list[i], 'pic': self._pic_list[i]}
            list_result.append(dict_carinfo)
            i += 1

@asyncio.coroutine
def getPicture(url):
    print("getting picture")

    if getProxyConfig("enable") == "1":
        # THE PROXY INFO
        proxy_uri = getProxyConfig('server')
        proxy_user = getProxyConfig('user')
        proxy_pwd = getProxyConfig('password')
        proxy_sever = 'http://'+proxy_uri
        conn = aiohttp.ProxyConnector(proxy=proxy_sever, proxy_auth=aiohttp.BasicAuth(proxy_user, proxy_pwd))
        response = yield from aiohttp.get(url, connector=conn)
    else:
        response = yield from aiohttp.get(url)
    return (yield  from  response.read())

@asyncio.coroutine
def getCarInfo(query_car):
    print("fetching %s-%s" % (query_car['make'], query_car['mode']))

    url = "http://wwwa.autotrader.ca/cars/%s/%s/on/toronto/?prx=100&prv=Ontario&loc=Toronto" \
          % (query_car['make'],query_car['mode']) + \
          "%2c+ON&body=SUV&sts=New&showcpo=1&hprc=True&wcp=True&srt=3&rcs=0&rcp=20"
    if getProxyConfig("enable") == "1":
        # THE PROXY INFO
        proxy_uri = getProxyConfig('server')
        proxy_user = getProxyConfig('user')
        proxy_pwd = getProxyConfig('password')
        proxy_sever = 'http://'+proxy_uri
        conn = aiohttp.ProxyConnector(proxy=proxy_sever, proxy_auth=aiohttp.BasicAuth(proxy_user, proxy_pwd))
        response = yield from aiohttp.get(url, connector=conn)
    else:
        response = yield from aiohttp.get(url)
    return( yield from response.text())


@asyncio.coroutine
def process(query_car):
    print("gen data start[%s-%s]" % (query_car["make"], query_car["mode"]))
    html = yield from getCarInfo(query_car)
    myparse = MyParser(query_car["make"], query_car["mode"])
    myparse.feed(html)
    myparse.merge()
    print("gen data complete[%s-%s]" % (query_car["make"], query_car["mode"]))

    ''' not effective
    #update 'pic' content to binary
    for car in list_result:
        pic= yield from getPicture(car['pic'])
        print(pic)
        car['pic']=pic
    '''


def execute():
    loop = asyncio.get_event_loop()
    tasks = [process(query_car) for query_car in query_list]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

    # write file
    print(list_result)
    if list_result == []:
        print("NO DATA!!")
        return
    write_excel(list_result)
    print("gen xls completed")




if __name__ == '__main__':

    start = time.clock()
    print("run main()")
    execute()
    end = time.clock()
    print("cost: %f s" % (end - start))