# -*- coding: utf-8 -*-

import string
from urllib import request
import re
import os
from bs4 import BeautifulSoup
import random
from multiprocessing import Process, Queue
import time
import threading
import logging

# 创建一个logger
logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)


# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('c:/test.log')

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()

# 定义handler的输出格式formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


class Baidu_Spider:
    # 申明相关的属性
    def __init__(self, url):
        self.myUrl = url
        self.datas = []
        self.list = Queue()
        self.maxPage = 0

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
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0) Gecko/20121026 Firefox/16.0',
            'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
            'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13',
            'Mozilla/5.0 (iPhone; U; CPU like Mac OS X) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3',
            'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13'
        ]
        logger.info('已经启动百度贴吧爬虫，咔嚓咔嚓')

    #获取http头部
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

    # http连接有问题时候，自动重连
    def conn_try_again(function):
        RETRIES = 1
        # 重试的次数
        count = {"num": RETRIES}
        def wrapped(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception as e:
                cnt = count['num']
                threadName = threading.current_thread().getName()
                if count['num'] < 11:
                    logger.warning("***********爬虫报告：爬虫%s通信发现错误，准备重试！重试次数：%d....." %(threadName,cnt))
                    count['num'] += 1
                    time.sleep(4)
                    return wrapped(*args, **kwargs)
                else:
                    logger.error('***********爬虫报告：爬虫%s通信发现错误,重试失败！！！！！！！！！！！！'%(threadName), e)
        return wrapped

    # 初始化加载页面并将其转码储存
    @conn_try_again
    def baidu_tieba(self):
        pn = 0
        try:
            max = self.maxPage
            while pn <= max:
                time.sleep(2)
                myheaders = self.get_header()
                url = self.myUrl + '&pn=' + str(pn)
                threadName = threading.current_thread().getName()
                req = request.Request(url, headers=myheaders)
                logger.info("***********爬虫报告：爬虫%s正在爬取一览页面%s" %(threadName,url))
                with request.urlopen(req, timeout=60) as f:
                    if f.getcode() != 200:
                        logger.warning("***********爬虫报告：爬虫%s通信发现错误，状态code：%s....." % (threadName, str(f.getcode())))
                        raise Exception

                    time.sleep(2)
                    pagelist = f.read().decode('utf-8')
                    #获取帖子
                    titlist = re.findall('<a href="(.*?)" title=.*?class="j_th_tit "', pagelist)
                    for tl in titlist:
                        self.list.put(tl)

                    pn = pn + 50
        except Exception as e:
            logger.warning('***********爬虫报告：爬虫%s爬取一览页面发生错误:'%(threadName),e)
            raise Exception

    #获取最大页数
    @conn_try_again
    def get_max_page(self):
        try:
            myheaders = self.get_header()
            url = self.myUrl + '&pn=0'
            req = request.Request(url, headers=myheaders)
            with request.urlopen(req, timeout=60) as f:
                if f.getcode() != 200:
                    threadName = threading.current_thread().getName()
                    logger.warning("***********爬虫报告：爬虫%s通信发现错误，状态code：%s....." %(threadName,str(f.getcode())))
                    raise Exception

                logger.info("***********爬虫报告：爬虫正在爬取最大页数中.....")
                time.sleep(2)
                homePage = f.read().decode('utf-8')
                lastPage = re.search(r'class="next pagination-item " >下一页(.*?)class="last pagination-item "',homePage,re.S);
                if lastPage:
                    maxPageUrl = lastPage.group(1)

                maxPageContent = re.search(r'pn=(\d+?)"',maxPageUrl,re.S);
                if lastPage:
                    self.maxPage = int(maxPageContent.group(1))

            logger.info("***********爬虫报告：爬取最大页数结束，最大页数为：%s"%(str(self.maxPage)))
        except Exception as e:
            logger.warning('***********爬虫报告：爬取最大页数出错！',e)
            raise Exception

    #爬取详细页
    @conn_try_again
    def get_page(self):
        try:
            while not self.list.empty():
                threadName = threading.current_thread().getName()
                logger.info('***********爬虫报告：爬虫%s正在执行，当前队列大小:%s' %(threadName,str(self.list.qsize())))
                url = self.list.get();
                url = 'http://tieba.baidu.com' + url
                myheaders = self.get_header()
                req = request.Request(url, headers=myheaders)
                with request.urlopen(req, timeout=60) as f:
                    if f.getcode() != 200:
                        threadName = threading.current_thread().getName()
                        logger.warning("***********爬虫报告：爬虫%s通信发现错误，状态code：%s....." % (threadName, str(f.getcode())))
                        raise Exception

                    logger.info("***********爬虫报告：爬虫%s正在爬取详细页面 url：%s"%(threadName,url))
                    time.sleep(2)
                    myPage = f.read().decode('utf-8')
                    # 计算楼主发布内容一共有多少页
                    endPage = self.page_counter(myPage)
                    # 获取该帖的标题
                    title = self.find_title(myPage)
                    logger.info('***********爬虫报告：爬虫%s爬取文章名称：%s'%(threadName,title))
                    # 获取最终的数据
                    self.get_data(url, endPage, title)
            logger.info('***********爬虫报告：爬虫%s完成任务！' % (threadName))
        except Exception as a:
            logger.warning('***********爬虫报告：爬虫%s爬取详细页出现异常，重启爬虫'%(threadName))
            raise Exception

    # 用来计算一共有多少页
    def page_counter(self, myPage):
        # 匹配 "共有<span class="red">12</span>页" 来获取一共有多少页
        myMatch = re.search(r'class="red">(\d+?)</span>', myPage, re.S)
        if myMatch:
            endPage = int(myMatch.group(1))
            logger.info('爬虫报告：发现楼主共有%d页的原创内容' % endPage)
        else:
            endPage = 0
            logger.warning('爬虫报告：无法计算楼主发布内容有多少页！')
        return endPage

    # 用来寻找该帖的标题
    def find_title(self, myPage):
        # 匹配 <h1 class="core_title_txt" title="">xxxxxxxxxx</h1> 找出标题
        myMatch = re.search(r'<h3.*?>(.*?)</h3>', myPage, re.S)
        title = '暂无标题'
        if myMatch:
            title = myMatch.group(1)
        else:
            logger.warning('爬虫报告：无法加载文章标题！')
        # 文件名不能包含以下字符： \ / ： * ? " < > |
        title = title.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"',
                                                                                                                    '').replace(
            '>', '').replace('<', '').replace('|', '')
        return title

    # 用来存储楼主发布的内容
    def save_data(self, url, title, endPage):
        # 加载页面数据到数组中
        self.get_data(url, endPage ,title)

    # 按页获取详细页面数据
    def get_data(self, url, endPage, title):
        for i in range(1, endPage + 1):
            pageUrl = url + '?see_lz=1' + '&pn=' + str(i)
            self.get_current_page_data(pageUrl, title, i)


    #获取帖子某一页数据
    @conn_try_again
    def get_current_page_data(self, url, title, currentPage):
        try:
            myheaders = self.get_header()
            req = request.Request(url, headers=myheaders)
            with request.urlopen(req, timeout=60) as f:
                threadName = threading.current_thread().getName()
                logger.info('爬虫报告：爬虫%s正在加载中第%d页中...' % (threadName, currentPage))
                if f.getcode() != 200:
                    threadName = threading.current_thread().getName()
                    logger.warning("***********爬虫报告：爬虫%s通信发现错误，状态code：%s....." % (threadName, str(f.getcode())))
                    raise Exception

                time.sleep(2)
                myPage = f.read().decode('utf-8')
                self.deal_data(myPage, title, url)
        except Exception as e:
            logger.warning('爬虫报告：爬虫%s加载详细页第%d页发生错误' % (threadName, currentPage))
            raise Exception


    # 将内容从页面代码中抠出来
    def deal_data(self, myPage, title, url):
        reg = r'class="BDE_Image"(.*?)src="([.*\S]*\.jpg)"'
        imgre = re.compile(reg);
        imglist = re.findall(imgre, myPage)

        if len(imglist) > 0:
            if not os.path.exists(r'd:/pic/'):
                os.mkdir(r'd:/pic/')

            path = 'd:/pic/' + title

            if not os.path.exists(r'd:/pic/'+title):
                os.makedirs(path)

            #保存图片
            imgName = 1
            for imgPath in imglist:
                localPath = path + "/" + str(imgName) + ".jpg"
                logger.info("图片url:" + imgPath[1])
                self.save_pic(imgPath[1], localPath)
                imgName += 1
                time.sleep(2)

            #记录帖子地址
            f = open(path + '/url.txt', 'w')
            f.write(str(url))
            f.close()

    #保存图片
    @conn_try_again
    def save_pic(self, impPath, path):
        try:
            threadName = threading.current_thread().getName()
            with open(path, 'wb') as f:
                time.sleep(1)
                req = request.Request(impPath)
                with request.urlopen(req, timeout=60) as pic:
                    logger.info('爬虫报告：爬虫%s正在加载图片中...' % (threadName))
                    if pic.getcode() != 200:
                        logger.warning("***********爬虫报告：爬虫%s通信发现错误，状态code：%s....." % (threadName, str(f.getcode())))
                        raise Exception

                    f.write(pic.read())
        except Exception as e:
            logger.warning('爬虫报告：爬虫%s加载图片发生错误' % (threadName),e)
            raise Exception

# -------- 程序入口处 ------------------
print (u"""#---------------------------------------
#   程序：百度贴吧爬虫
#   版本：0.1
#   作者：sx
#   日期：2016-09-17
#   语言：Python 3.5
#   操作：------------------------------
#   功能：下载贴吧内所有帖子的图片。
#---------------------------------------
""")
witeFlg = True
while witeFlg:
    bdurl = input('请输入贴吧地址(http://tieba.baidu.com/f?kw=)：')

    if bdurl.strip() == '':
        logger.info('输入为空！默认下载漫画分享吧资源！')
        bdurl = 'http://tieba.baidu.com/f?kw=%E6%BC%AB%E7%94%BB%E5%88%86%E4%BA%AB&ie=utf-8'
        witeFlg = False
        continue

    if bdurl == 'quit' or bdurl == 'exit':
        exit()

    result = re.search(r'http://tieba.baidu.com\/f\?kw\=(.*?)', bdurl)
    if result == None:
        logger.info('输入的地址格式有误,请重新输入！')
        continue

    witeFlg = False

logger.info('入口地址：' + bdurl)
time.sleep(2)
# 调用
mySpider = Baidu_Spider(bdurl)
#取最大页数
mySpider.get_max_page()
#检查最大页数
if mySpider.maxPage == 0:
    logger.warning('没有找到最大页数，请检查网址是否正确')
    exit()

#爬取一览页帖子
t = threading.Thread(target=mySpider.baidu_tieba, name='listThread')
t.start()
time.sleep(20)

#多进程
for i in range(1,5):
    s = threading.Thread(target=mySpider.get_page, name='subThread'+ str(i))
    time.sleep(4)
    logger.info('爬虫报告：爬虫%d号启动...' % i)
    s.start()