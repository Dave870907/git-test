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
    div = soup.find('div',{'id':'main-container'})
    items = soup.findAll('div',{'class':'r-ent'})
    
    for i in items:
        URL = i.find('div',{'class':'title'})
        a = URL.find('a')
        website = "https://www.ptt.cc"+ a.get('href')
        url_list.append(website)
    # print(url_list)
def getContent():
    #順便寫入資料庫
    
    for url in url_list:
        content = ''
        res = requests.get(url,cookies={'over18': '1'})
        if res.status_code == 200:
            body = res.content
            soup = BeautifulSoup(body, "html.parser")
            # 要怎麼得到乾淨的網站內文字
            # 用bs4清理
            
            #他在這個div裡面用一堆p跟br包，所以直接取text
            article = soup.find('div',{'id':'main-container'})
            article_div = article.findAll('div')
            for p in article_div:
                if str(p.text)!= 'None':
                    content += str(p.text)  
            
           
        # print(content)
        content = content.lstrip()
        cursor.execute("create table if not exists resultMoney (ID INTEGER PRIMARY KEY   AUTOINCREMENT,source text, URL text, content text) ") 
        sql = "insert into resultMoney (source,URL,content ) values ('PTT','"+ url +"','"+ content + "')" 
        sql2 = "DELETE from resultMoney where ID NOT IN (Select Max(ID) From resultMoney Group By URL)"    #刪除重複的資料      
      
        cursor.execute(sql)
        cursor.execute(sql2)
        connection.commit()  
def pttMoney(pagenum,keyword):
    
    for i in range(1,pagenum):  #range決定跑幾頁

        #搜尋條件
        

        url ='https://www.ptt.cc/bbs/Lifeismoney/search?page='+str(i)+'&q='+ keyword
        
        r = requests.get(url,cookies={'over18': '1'})
        getUrl(r)

    getContent()
    # print(url)
# pttMoney(2,'寶雅')