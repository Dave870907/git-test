import requests
from bs4 import BeautifulSoup

import urllib.parse
import sqlite3

url_list = []

#資料庫連線
connection = sqlite3.connect('search_Result.db')
cursor = connection.cursor()

#取得網址列表
def getUrl(r) :
    content = r.content
    soup = BeautifulSoup(content, "html.parser")
    div = soup.find('div',{'class':'search_list_div'})
    link_a = div.findAll("a")
    for i in link_a:
        
        href = i.get('href')
        url_list.append(href)
    
def getContent():
    #順便寫入資料庫
    
    for url in url_list:
        content = ''
        res = requests.get(url)
        if res.status_code == 200:
            body = res.content
            soup = BeautifulSoup(body, "html.parser")
            # 要怎麼得到乾淨的網站內文字
            # 用bs4清理
            
            #他在這個div裡面用一堆p跟br包，所以直接取text
            article = soup.find('div',{'class':'h7 margin_b20'})
            article_ps = article.findAll('p') 
            for j in article_ps:
                content += str(j.text) 
            
            article_br = article.findAll('br')
            for i in article_br:
                content += str(i.text)  
            article_div = article.findAll('div')
            for k in article_div:
                # content += str(k.text)
                article_ps2 = k.findAll('p')
                for p in article_ps2:
                    content += str(p.text)
                article_br2 = k.findAll('br')
                for br in article_br2:
                    content += str(br.text)
              
        content = content.lstrip()
        # print(content)
        cursor.execute("create table if not exists resultTVBS (ID INTEGER PRIMARY KEY   AUTOINCREMENT,source text, URL text, content text) ")
        sql ="insert into resultTVBS (source,URL,content ) values ('TVBS','"+ url +"','"+ content + "')"
        sql2 = "DELETE from resultTVBS where ID NOT IN (Select Max(ID) From resultTVBS Group By URL)"
        cursor.execute(sql)
        cursor.execute(sql2)
        connection.commit()
def TVBSclimb(pagenum,keyword):
    for i in range(1,pagenum):  #range決定跑幾頁
        key = keyword
        url ='https://news.tvbs.com.tw/news/searchresult/news/'+ str(i) +'/?search_text='+ key
        r = requests.get(url)
        getUrl(r)
        # print(url_list)
    getContent()
# TVBSclimb(2,'口罩')