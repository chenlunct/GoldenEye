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
    def __init__(self,blogtype = 0):
        # 0 for SinaBlog
        # 1 for Xueqiu
        self.BlogType = blogtype
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
                if u"暂无博文".encode('gbk') in pagestring:
                    return itemList
                try:
                    pagedata = etree.HTML(pagestring.decode('gbk','ignore'))
                    itemList.extend(pagedata.xpath(u"//div[@class='blog_title']/a/@href"))
                except:
                    print "page analyze error:"
                    print pagestring

        elif self.BlogType == 1:
            p0 = re.compile(r"\d+")
            try:
                userid = p0.findall(blogurl)[0]
            except:
                print "wrong url: ",blogurl

            for page in range(1,50):
                pagestring = self.TryGetPage("http://xueqiu.com/statuses/user_timeline.json?user_id="+str(userid)+"&page="+str(page))

                try:
                    jsondata = self.parse_js(pagestring)
                    if int(jsondata["page"]) > int(jsondata["maxPage"]):
                        return itemList
                    statuslist = jsondata["list"]
                    for status in statuslist:
                        resultrow = []
                        if status["retweet_status_id"]==0:
                            stocklist = self.hasStock(status["description"])
                        else:
                            stocklist = self.hasStock(status["description"]+status["retweeted_status"]["description"]+status["retweeted_status"]["title"])
                        if stocklist == []:
                            continue
                        resultrow.append(str(status["id"]))
                        resultrow.append(status["created_at"])
                        resultrow.append(str(status["user_id"]))
                        resultrow.append(stocklist)
                        itemList.append(resultrow)
                except:
                    print "page analyze error:"
                    print pagestring

        return itemList

    # return a list of stocks if the input text has stocks
    # Example:[SH000001]
    # if there is no stock in text
    # retuen []
    def hasStock(self, text):
        p0 = re.compile(r"(?<=\()SH\d{6}(?=\))")
        p1 = re.compile(r"(?<=\()SZ\d{6}(?=\))")
        stocklist = []
        stocklist.extend(p0.findall(text))
        stocklist.extend(p1.findall(text))
        return list(set(stocklist))

    def parse_js(self,expr):
        import ast
        m = ast.parse(expr)
        a = m.body[0]
        def parse(node):
            if isinstance(node, ast.Expr):
                return parse(node.value)
            elif isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.Str):
                return node.s
            elif isinstance(node, ast.Name):
                return node.id
            elif isinstance(node, ast.Dict):
                return dict(zip(map(parse, node.keys), map(parse, node.values)))
            elif isinstance(node, ast.List):
                return map(parse, node.elts)
            else:
                raise NotImplementedError(node.__class__)
        return parse(a)

if __name__ == '__main__':
    # c = core()
    # print c.GetItemList("http://blog.sina.com.cn/u/1491999985")
    c = core(1)
    # print c.hasStock("(SH600104):上汽集团计划提升,九阳股份(SZ002242):九阳股份(SZ002242)九阳股份(SZ002242)九阳股份(SZ002242)$格力电器(SZ000651)$ 新")
    c.GetItemList("http://xueqiu.com/7279006625")