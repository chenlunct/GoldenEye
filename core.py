#coding=utf-8
# core procs for crawling data

import urllib
import urllib2
import yaml
import time
import cookielib
import commands
import re
import json
import copy
import lxml

class core:
    def __init__(self):
        # 0 for SinaBlog
        self.BlogType = 0
        file = open('config.yml')
        self.config_data = yaml.load(file)
        file.close()
        enable_proxy = self.config_data['enable_proxy']
        self.cj = cookielib.LWPCookieJar()
        self.cookie_support = urllib2.HTTPCookieProcessor(self.cj)
        proxy_handler = urllib2.ProxyHandler({'http': self.config_data['proxy_address']})
        null_proxy_handler = urllib2.ProxyHandler({})

        if enable_proxy:
            opener = urllib2.build_opener(self.cookie_support,proxy_handler)
        else:
            opener = urllib2.build_opener(self.cookie_support,null_proxy_handler)
        urllib2.install_opener(opener)

    def TryGetPage(self, url, data=None, referer=None,retry=5):
        i = 0
        while i < retry:

            if data is None:
                req = urllib2.Request(url)
            else:
                req = urllib2.Request(url, data)
            req.add_header('User-Agent', "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36")
            req.add_header('Connection','keep-alive')
            if referer != None:
                req.add_header('Referer',referer)
            # req.add_header('Accept',"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
            # req.add_header('Accept-Encoding'," gzip,deflate,sdch")
            # req.add_header('Accept-Language'," zh-CN,zh;q=0.8,en;q=0.6")

            response = urllib2.urlopen(req,timeout=20)
            page = response.read()

            if len(page) != 0:
                break
            else:
                time.sleep(0.2)
                i = i+1

        return page

    # blogurl: url should be the formart as "http://blog.sina.com.cn/u/1491999985"
    def GetItemList(self, blogurl):
        from lxml import etree
        itemList = []
        if self.BlogType == 0:
            p0 = re.compile(r"\d+")

            try:
                userid = p0.findall(blogurl)[0]
            except:
                print "wrong url: ",blogurl

            for page in range(0,10):
                pagestring = self.TryGetPage("http://blog.sina.com.cn/s/article_sort_"+str(userid)+"_10001_"+str(page)+".html")
                try:
                    pagedata = etree.HTML(pagestring.decode('gbk','ignore'))
                    itemList.extend(pagedata.xpath(u"//div[@class='blog_title']/a/@href"))
                except:
                    print "page analyze error:"
                    print pagestring
                # if u"没有对应的宝贝".encode('gbk') in pagestring or u"很抱歉，搜索到".encode('gbk') in pagestring:
                #     return sorted(set(itemList),key=itemList.index)
        elif self.BlogType == 1:
            # future use for other blogs
            pass
        print itemList
        return itemList


if __name__ == '__main__':
    c = core()
    print c.GetItemList("http://blog.sina.com.cn/u/1491999985")