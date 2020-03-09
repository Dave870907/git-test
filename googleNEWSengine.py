#encoding=utf-8
import jieba
import csv
import codecs
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import urllib
import re

# 勉強可跑
search_list = [] #儲存網址
content_list = [] #儲存網頁內容
keyword = quote('"口罩"'.encode('utf8'))
user_agent = {"user_agent" :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
# 搜尋結果好像不太對
res = requests.get("https://www.google.com.tw/search?num=10&q="+keyword+"&oq="+keyword+"&dcr=0&tbm=nws&source=lnt&tbs=qdr:d",headers = user_agent)

# 關鍵字多加一個雙引號是精準搜尋
# num: 一次最多要request的筆數, 可減少切換頁面的動作
# tbs: 資料時間, hour(qdr:h), day(qdr:d), week(qdr:w), month(qdr:m), year(qdr:w)
def cal(sentence):  #計數丟進CSV
    i = 0 
    hash1 = {}
    word_list = []
    jieba.set_dictionary('dict.txt.big')
    jieba.load_userdict("userdict.txt") #加入自訂文字庫
    # sentence = "獨立音樂需要大家一起來推廣，歡迎加入我們的行列獨立！"
    print ("Input：", sentence)
    words = jieba.cut(sentence, cut_all=False)
    print ("Output 精確模式 Full Mode：")
    for word in words:
        print (word)
        #把字加進list
        word_list.append(word)
    for item in word_list:
        if item in hash1 :
            hash1[item] += 1
        else :
            hash1.update({item:1})
    print (hash1)
    #寫入CSV
    fd = open("count.csv","w",encoding="utf-8")
    fd.write("word,count\n")
    for k in hash1 :
        fd.write("%s,%d\n"%(k,hash1[k]))
def gethref():   #得到網址用
    if res.status_code == 200:
        content = res.content
        soup = BeautifulSoup(content, "html.parser")
        # print (soup.prettify())
        items = soup.findAll("div", {"class": "kCrYT"})
        for item in items:
            href = item.find("a")
            if href != None:
                href = href.get('href')
                #去掉網址前面7個字
                news_href = href[7:]
            search_list.append(news_href)
    for i in search_list:
        print(i)
def getContent():
    gethref()
    test1 = ''
    for i in search_list:
        res = requests.get(i)
        if res.status_code == 200:
            content = res.content
            soup = BeautifulSoup(content, "html.parser")
            
            # 要怎麼得到乾淨的網站內文字
            items = soup.get_text()
            content_list.append(items)
    for i in content_list:  #清理多餘的英文字
        r1 = '[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
        string1 = re.sub(r1,"",i)
        string2 = re.sub('\s','',string1)
        test1 += string2
    cal(test1)
    # print(content_list)

getContent()
