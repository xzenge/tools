#-*- coding: utf-8 -*-

from urllib import request
import os
from bs4 import BeautifulSoup
import string
import re
import datetime

# url = input("网站地址:")

url = "http://www.proxy360.cn/default.aspx"

headers = { 'User-Agent' : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding' : 'gzip, deflate, sdch',
            'Accept-Language' : 'zh-CN,zh;q=0.8',
            'Cache-Control' : 'max-age=0',
            'Connection' : 'keep-alive',
            'Host' : 'www.xicidaili.com',
            'Referer' : 'https://www.baidu.com/link?url=hmj1JZYNYN7lIBvk5s7FSmM1FNEzxf_C7ass2zNM0miVclY9_TVwrHmgSqxIukCH&wd=&eqid=97e797a400041b130000000457cd3262',
            'Upgrade-Insecure-Requests' : '1'}
pox_list = []
req = request.Request(url)
with request.urlopen(req, timeout= 120) as f:
    html = f.read().decode('utf-8')
    soup = BeautifulSoup(html)
    cont = soup.find_all('div', id='ctl00_ContentPlaceHolder1_upProjectList')
    list = BeautifulSoup(str(cont))
    result = list.find_all('div',class_='proxylistitem')

    for r in result:
        text = r.text
        text = text.replace('\r\n','').replace('\n', '').lstrip()
        contlist = re.split('\s+',text)
        pox = (contlist[0],contlist[1])
        pox_list.append(pox)

    t = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    file = open('d:/poxy/poxy_' + t + '.txt', 'w')
    for px in pox_list:
        pxw = 'http://' + px[0] + ':' + px[1] + '/'
        file.write(pxw)
        file.write('\n')
    file.close()

    print(pox_list)
