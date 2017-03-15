
# -*- coding: utf-8 -*-
"""
--百度爬虫
--by Paul
--2017/2/22
"""

import requests
from bs4 import BeautifulSoup
import csv
import codecs

def buildRequestString(key, keyWords):
    keyWordsString = ''
    if(len(keyWords)==1):
        keyWordsString = keyWords[0]
    if(len(keyWords)==0):
        keyWordsString = ""
    if(len(keyWords)>1):
        for index in range(len(keyWords)):
            keyWordsString = keyWordsString + keyWords[index] + "+"
        keyWordsString = keyWordsString[0:len(keyWordsString)-1]
    print keyWordsString

    requestString = "https://www.baidu.com/s?q1=&q2=%s&q3=%s&q4=&gpc=stf&ft=&q5=&q6=&tn=baiduadv"%(key,keyWordsString)
    print requestString
    return requestString

def parseItems(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
    }
    Items = []
    try:
        response = requests.get(url, headers=headers)
        try:
            soupPage = BeautifulSoup(response.text, 'lxml')
            pageListItems = soupPage.find_all('div', attrs={"class": "result c-container "})
            print len(pageListItems)

            for pageItem in pageListItems:
                Item = []
                a = pageItem.find_all('a')[0]

                Item.append(a['href'])
                Item.append(a.get_text().encode('UTF-8'))

                abstract = pageItem.find_all('div', attrs={"class": "c-abstract"})[0]

                Item.append(abstract.get_text().encode('UTF-8'))

                Items.append(Item)
        except Exception as e:
            print e.message

    except Exception as e:
        print e.message
    return Items


if __name__=="__main__":
    key = "济南华洛汽车部件有限公司"
    keyWords = []
    keyWords.append("反洗钱")
    keyWords.append("贪污")
    keyWords.append("诉讼")
    requestUrl = buildRequestString(key, keyWords)
    url='http://www.baidu.com/link?url=AgyBsqK7IhZaGJXxU8rHrGN7L_Lxqb88xz8O4tvTOFeibtaB1uiAmM4W6L44nB1_Ochu7PwndTWgnkXX_1q2Wq'
    Items = parseItems(url)

    # --------------------------------------------------------------Start Write
    try:
        csvfile = file('BaiduSearch.csv', 'wb')
        csvfile.write(codecs.BOM_UTF8)
        writer = csv.writer(csvfile)
        writer.writerow(['Link', 'Title', 'abstract'])
        for line in Items:
            print line
            writer.writerow(line)
        csvfile.close()
    except Exception as e:
        print "Write File Error: " + e.message
        # --------------------------------------------------------------End Write







