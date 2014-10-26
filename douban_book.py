# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 20:02:49 2014

@author: aneasystone
@description: for crawling the detail information of my douban wish books
"""

import urllib2
import re
import time

# user fiddler to debug
proxy = '127.0.0.1:8888'

def main():
    books = []
    
    # recursively fetch the books
    nextPage = 'http://book.douban.com/people/aneasystone/wish'
    html = url_get(nextPage, 'utf-8', proxy)
    books.extend( parse_books(html) )
    nextPage = get_next_page(html)
    return
    while nextPage != None:
        print 'opening next page: %s' % nextPage
        time.sleep(5)
        html = url_get(nextPage, 'utf-8', proxy)
        books.extend( parse_books(html) )
        nextPage = get_next_page(html)
    
    # print all books
    for book in books:
        print book.toString()

def parse_books(html):
    
    # get all urls
    bookUrls = []
    matches = re.findall(
        u'<li class="subject-item".*?<div class="pic".*?<a class="nbg" href="([^"]*)"', html, re.S|re.I)
    for match in matches:
        bookUrls.append(match)
        
    # walk the urls to fetch the details
    books = []
    for url in bookUrls:
        book = parse_book_detail(url)
        print book.toString()
        books.append(book)
        
    return books
    
def parse_book_detail(url):

    # fetch the detail html    
    html = url_get(url, 'utf-8', proxy)    
    
    # title
    title = ''
    titleReg = u'<span property="v:itemreviewed">(.*?)</span>'    
    m = re.search(titleReg, html, re.S|re.I)
    if m != None:
        title = m.group(1)
        
    # info: author, pages
    author = ''
    pages = ''
    infoReg = u'<span class="pl".*?作者.*?<a.*?>(.*?)</a>.*?<span class="pl".*?页数.*?(\d+)<br>'
    m = re.search(infoReg, html, re.S|re.I)
    if m != None:
        author = m.group(1)
        pages = m.group(2)
        
    # score
    score = ''
    scoreReg = u'<strong class="ll rating_num.*?([0-9.]+).*?</strong>'
    m = re.search(scoreReg, html, re.S|re.I)
    if m != None:
        score = m.group(1)
    
    return DoubanBook(title, author, pages, score, url)

def get_next_page(html):
    match = re.search(u'<a href="([^"]*)".*后页&gt;.*</a>', html, re.M|re.I)
    nextPage = None    
    if match:
        nextPage = match.group(1)
    return nextPage

'''
usage:
    url_get('http://www.baidu.com')
    url_get('http://www.baidu.com', 'utf-8')
    url_get('http://www.baidu.com', 'utf-8', '192.168.0.101:3128')
'''
def url_get(url, encoding='utf-8', proxy=None):
    
    # use proxy
    proxyHandler = urllib2.ProxyHandler({})
    if proxy != None:
        proxyHandler = urllib2.ProxyHandler({
            'http': 'http://' + proxy
        })
    opener = urllib2.build_opener(proxyHandler)
    urllib2.install_opener(opener)
    
    # set http headers
    headers = {
        'Host': 'book.douban.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
        'Referer': 'http://book.douban.com/people/aneasystone/wish',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cookie': 'dbcl2="2029399:WBEnawaXYKs"; ct=y; ck="FrLx"; bid="/2S/YMF0xbk"; __utmt_douban=1; __utmt=1; push_noty_num=0; push_doumail_num=0; __utma=30149280.665181411.1408466728.1414323988.1414328453.35; __utmb=30149280.7.10.1414328453; __utmc=30149280; __utmz=30149280.1408466728.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=30149280.202; __utma=81379588.327322834.1408466728.1414323988.1414328453.35; __utmb=81379588.7.10.1414328453; __utmc=81379588; __utmz=81379588.1408466728.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _pk_id.100001.3ac3=f412f0a360ff8243.1408466728.35.1414331606.1414325593.; _pk_ses.100001.3ac3=*'
    }
    
    # requesting
    request = urllib2.Request(url, headers = headers)
    res = urllib2.urlopen(request)
    html = res.read().decode(encoding, errors='ignore')
    res.close()
    return html

class DoubanBook:
    
    title = ''
    author = ''
    pages = ''
    score = ''
    url = ''
    
    def __init__(self, title, author, pages, score, url):
        self.title = title
        self.author = author
        self.pages = pages
        self.score = score
        self.url = url
    
    def toString(self):
        return '%s, %s, %s, %s' % (self.title, self.author, self.pages, self.score)

if __name__ == "__main__":
    main()
