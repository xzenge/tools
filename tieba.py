# -*- coding: utf-8 -*-
# ---------------------------------------
#   程序：百度贴吧爬虫
#   版本：0.5
#   作者：why
#   日期：2013-05-16
#   语言：Python 2.7
#   操作：输入网址后自动只看楼主并保存到本地文件
#   功能：将楼主发布的内容打包txt存储到本地。
# ---------------------------------------

import string
from urllib import request
import re
import os
from bs4 import BeautifulSoup
import random
from multiprocessing import Process, Queue
import time
import threading

# ----------- 处理页面上的各种标签 -----------
class HTML_Tool:
    # 用非 贪婪模式 匹配 \t 或者 \n 或者 空格 或者 超链接 或者 图片
    BgnCharToNoneRex = re.compile("(\t|\n| |<a.*?>|<img.*?>)")

    # 用非 贪婪模式 匹配 任意<>标签
    EndCharToNoneRex = re.compile("<.*?>")

    # 用非 贪婪模式 匹配 任意<p>标签
    BgnPartRex = re.compile("<p.*?>")
    CharToNewLineRex = re.compile("(<br/>|</p>|<tr>|<div>|</div>)")
    CharToNextTabRex = re.compile("<td>")

    # 将一些html的符号实体转变为原始符号
    replaceTab = [("<", "<"), (">", ">"), ("&", "&"), ("&", "\""), (" ", " ")]

    def Replace_Char(self, x):
        x = self.BgnCharToNoneRex.sub("", x)
        x = self.BgnPartRex.sub("\n    ", x)
        x = self.CharToNewLineRex.sub("\n", x)
        x = self.CharToNextTabRex.sub("\t", x)
        x = self.EndCharToNoneRex.sub("", x)

        for t in self.replaceTab:
            x = x.replace(t[0], t[1])
        return x


class Baidu_Spider:
    # 申明相关的属性
    def __init__(self, url):
        # self.myUrl = url + '?see_lz=1'
        self.myUrl = url
        self.datas = []
        self.myTool = HTML_Tool()
        self.list = Queue()

        self.userAgents = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER) ',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)" ',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E) ',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400) ',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E) ',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE) ',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E) ',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E) ',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E) ',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E) ',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E) ',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) ',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0) Gecko/20121026 Firefox/16.0'
        ]
        print (u'已经启动百度贴吧爬虫，咔嚓咔嚓')


    def get_header(self):
        user_agent = random.choice(self.userAgents)
        myheaders = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            # 'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'tieba.baidu.com',
            'Cookie' : 'BAIDUID=B1FC12619793B7F7B8372DF628173A5B:FG=1; BIDUPSID=B1FC12619793B7F7B8372DF628173A5B; PSTM=1458541218; TIEBA_USERTYPE=69b534f8b4daa3910d852aff; bdshare_firstime=1458549202847; BDUSS=RUbUJvTnYtSmFtR1huLUhHT35YQXRiQThJWmdUQjZkTVU5UFNLU2g5QXRUeTFYQVFBQUFBJCQAAAAAAAAAAAEAAAB20iQ4eHplbmdlAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAC3CBVctwgVXcn; TIEBAUID=7357fc7f96ce949abbe32dfc; rpln_guide=1; __cfduid=da22f9be5f02f610635d9c3f8e22b76c81461035795; MCITY=-289%3A; showCardBeforeSign=1; BCLID=6176374092207293183; BDSFRCVID=PbDsJeC62icXjNrRz1Hu-qFHjetrB_5TH6aocP-cVp5q56oA-3GKEG0Pfx8g0Ku-TBoLogKK0eOTHkQP; H_BDCLCKID_SF=tRCDoIPXJKI3fP36q45qMtK8hxtX5-RLfaRaKPOF5l8-hRTnW-6FKlDhDt7teRolWIQ-LPoPXK5xOKQphPbmqttZKaoDt65y04DeKhvN3KJme4P9bT3v5Du7Lxnr2-biWbR-2Mbd2MjmbRO4-TF-jjQb3e; wise_device=0; H_PS_PSSID=1444_18281_18134_17001_20856_20733_20837_20781; LONGID=941937270',
            'Upgrade-Insecure-Requests': '1'
        }
        return myheaders

    # 初始化加载页面并将其转码储存
    def baidu_tieba(self):
        ext = True
        pn = 0
        try:
            while ext:
                myheaders = self.get_header()
                url = self.myUrl + str(pn)
                req = request.Request(url, headers=myheaders)
                with request.urlopen(req, timeout=60) as f:
                    print("***********正在爬取一览页面：" + url)
                    time.sleep(2)
                    pagelist = f.read().decode('utf-8')
                    #获取帖子
                    self.get_PageList(pagelist)
                    pn = pn + 50
                    if pn > 7000:
                        ext = False
        except Exception as e:
            print('Error:',e)


    def get_page(self):
        try:
            while not self.list.empty():
                print('子任务执行  当前队列大小:' + str(self.list.qsize()))
                url = self.list.get();
                url = 'http://tieba.baidu.com' + url
                myheaders = self.get_header()

                req = request.Request(url, headers=myheaders)
                with request.urlopen(req, timeout=60) as f:
                    threadName = threading.current_thread().getName()
                    print("***********爬虫报告：爬虫%s正在爬取详细页面 url：%s"%(threadName,url))
                    time.sleep(2)
                    myPage = f.read().decode('utf-8')
                    # 计算楼主发布内容一共有多少页
                    endPage = self.page_counter(myPage)
                    # 获取该帖的标题
                    title = self.find_title(myPage)
                    print('***********爬虫报告：爬虫%s爬取文章名称：%s'%(threadName,title))
                    # 获取最终的数据
                    self.save_data(url, title, endPage)

        except Exception as a:
            print('***********爬虫报告：爬虫%s出现异常，重启爬虫'%(threadName))
            s = threading.Thread(target=mySpider.get_page, name=threadName)
            time.sleep(2)
            print('爬虫报告：爬虫%s启动...' % threadName)
            s.start()



    # 用来计算一共有多少页
    def page_counter(self, myPage):
        # 匹配 "共有<span class="red">12</span>页" 来获取一共有多少页
        myMatch = re.search(r'class="red">(\d+?)</span>', myPage, re.S)
        if myMatch:
            endPage = int(myMatch.group(1))
            print (u'爬虫报告：发现楼主共有%d页的原创内容' % endPage)
        else:
            endPage = 0
            print (u'爬虫报告：无法计算楼主发布内容有多少页！')
        return endPage

    # 用来寻找该帖的标题
    def find_title(self, myPage):
        # 匹配 <h1 class="core_title_txt" title="">xxxxxxxxxx</h1> 找出标题
        myMatch = re.search(r'<h3.*?>(.*?)</h3>', myPage, re.S)
        title = u'暂无标题'
        if myMatch:
            title = myMatch.group(1)
        else:
            print (u'爬虫报告：无法加载文章标题！')
        # 文件名不能包含以下字符： \ / ： * ? " < > |
        title = title.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"',
                                                                                                                    '').replace(
            '>', '').replace('<', '').replace('|', '')
        return title

    # 用来存储楼主发布的内容
    def save_data(self, url, title, endPage):
        # 加载页面数据到数组中
        self.get_data(url, endPage ,title)

    # 获取页面源码并将其存储到数组中
    def get_data(self, url, endPage, title):
        for i in range(1, endPage + 1):
            pageUrl = url + '?see_lz=1' + '&pn=' + str(i)
            threadName = threading.current_thread().getName()
            print ('爬虫报告：爬虫%s正在加载中第%d页中...'%(threadName,i))
            myheaders = self.get_header()
            req = request.Request(pageUrl, headers=myheaders)
            with request.urlopen(req, timeout=60) as f:
                time.sleep(2)
                myPage = f.read().decode('utf-8')
                # 将myPage中的html代码处理并存储到datas里面
                self.deal_data(myPage, title, url)

    # 将内容从页面代码中抠出来
    def deal_data(self, myPage, title, url):
        reg = r'class="BDE_Image"(.*?)src="([.*\S]*\.jpg)"'
        imgre = re.compile(reg);
        imglist = re.findall(imgre, myPage)

        if len(imglist):

            if not os.path.exists(r'd:/pic/'):
                os.mkdir(r'd:/pic/')

            path = 'd:/pic/' + title

            if not os.path.exists(r'd:/pic/'+title):
                os.makedirs(path)
            else:
                return

            imgName = 1

            for imgPath in imglist:
                path = path + "/"
                f = open(path + str(imgName) + ".jpg", 'wb')
                f.write((request.urlopen(imgPath[1])).read())
                f.close()
                imgName += 1
                time.sleep(1)

            f = open(path + 'url.txt', 'w')
            f.write(str(url))
            f.close()


    def get_PageList(self, pageList):
        soup = BeautifulSoup(pageList)
        content = soup.find_all(id='content')

        contentsoup = BeautifulSoup(str(content))
        titlist = contentsoup.find_all('a',class_='j_th_tit ')
        for tl in titlist:
            href = tl['href']
            # print('*****************href:' + href)
            self.list.put(href)



# -------- 程序入口处 ------------------
print (u"""#---------------------------------------
#   程序：百度贴吧爬虫
#   版本：0.1
#   作者：sx
#   日期：2016-09-17
#   语言：Python 3.5
#   操作：输入网址后自动只看楼主并保存到本地文件
#   功能：将楼主发布的内容打包txt存储到本地。
#---------------------------------------
""")

# 以某小说贴吧为例子
# bdurl = 'http://tieba.baidu.com/p/2296712428?see_lz=1&pn=1'

print (u'请输入贴吧的地址最后的数字串：')
# bdurl = 'http://tieba.baidu.com/' + str(raw_input(u'http://tieba.baidu.com/'))
bdurl = 'http://tieba.baidu.com/f?kw=%E6%BC%AB%E7%94%BB%E5%88%86%E4%BA%AB&ie=utf-8&pn='
# 调用
mySpider = Baidu_Spider(bdurl)
t = threading.Thread(target=mySpider.baidu_tieba, name='MainThread')
t.start()
time.sleep(15)
#多进程
for i in range(1,5):
    s = threading.Thread(target=mySpider.get_page, name='subThread'+ str(i))
    time.sleep(2)
    print(u'爬虫报告：爬虫%d号启动...' % i)
    s.start()



