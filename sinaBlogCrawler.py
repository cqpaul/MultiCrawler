# -*- coding: utf-8 -*-
#@FileName: xinLangBlog
#@Author  : Paul Zhang
#@Date    : 2017-03-15 11:01:23

import requests
from bs4 import BeautifulSoup
import time
import math
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
}

host = "127.0.0.1"
user = "paul"
password = "123456"
database = "aml"

# 通过博客数量计算页面数量，并返回每个页面的URL
# http://blog.sina.com.cn/s/articlelist_1374505811_0_4.html
def buildPageUrlList(articalListId, num):
    pageNum = int(math.ceil(num/50))+1
    urlList = []
    for i in range(1,pageNum+1):
        url = "http://blog.sina.com.cn/s/articlelist_{}_0_{}.html".format(articalListId,i)
        urlList.append(url)
    print urlList
    return urlList

def getPageListBlogInfo(url):
    blogItemList = []
    try:
        response = requests.get(url, headers)
        pageSoup = BeautifulSoup(response.text.encode(response.encoding).decode("utf-8"), 'lxml')
        divList = pageSoup.find_all("div", attrs={"class": "articleCell SG_j_linedot1"})
        for div in divList:
            aItem = div.find("a")
            blogUrl = aItem['href']
            blogTime = div.find("span", attrs={"class": "atc_tm SG_txtc"}).get_text()
            blog = getBlogPageInfo(blogUrl)
            blogInfo = {}
            blogInfo['blogurl'] = blogUrl
            blogInfo['blogtime'] = blogTime
            blogInfo["blogtitle"] = blog["title"]
            blogInfo["blogbody"] = blog["body"]
            blogInfo['blogType'] = "Sina"
            blogItemList.append(blogInfo)
    except Exception as e:
        print "Failed: " + url
        print e.message
    return blogItemList

#爬取每个blog的详情页
def getBlogPageInfo(url):
    blog = {}
    try:
        response = requests.get(url,headers=headers)
        soupPage = BeautifulSoup(response.text.encode(response.encoding).decode('utf-8'), 'lxml')
        blogTitle = soupPage.title.get_text()
        blog["title"] = blogTitle
        # print blogTitle
        divBody = soupPage.find('div', attrs={"id": "sina_keyword_ad_area2"})
        blogBody = divBody.get_text().replace('\t','').replace('\n','').replace(' ','')
        blog["body"] = blogBody
        # print blogBody
    except Exception as e:
        print "Failed: " + url
        print e.message
    return blog

if __name__=="__main__":
    db = MySQLdb.connect(host, user, password, database, charset='utf8')
    cursor = db.cursor()
    blogList = []
    pageUrlList = buildPageUrlList(1421819562, 3363)
    for url in pageUrlList:
        blogItemList = getPageListBlogInfo(url)
        print "finished one page.."
        blogList.extend(blogItemList)
    #将数据更新到数据库
    for item in blogList:
        try:
            sqlstr = "INSERT INTO sinablog(blogUrl,blogTitle,blogType,blogDate,blogBody) VALUES ('%s', '%s', '%s', '%s', '%s')" % (
                item["blogurl"], item["blogtitle"].encode('UTF-8'), item["blogType"], item["blogtime"],
                item["blogbody"].encode('UTF-8'))
            sqlstr = sqlstr.encode('UTF-8')
            cursor.execute(sqlstr)
            db.commit()
        except Exception as e:
            print "failed: " + item['blogurl']
            continue

    db.close()

