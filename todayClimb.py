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
    div = soup.find('div',{'class':'searchitem'})
    items = div.findAll('div',{'class':'searchitem__item'})
    
    for i in items:
        tag_a = i.find('a')
        href = tag_a.get('href')
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
            article = soup.find('div',{'itemprop':'articleBody'})
            article_ps = article.findAll('p')
            for p in article_ps:
                if str(p.text)!= 'None':
                    content += str(p.text)  
            
           
              
        content = content.lstrip()
        cursor.execute("create table if not exists resultToday (ID INTEGER PRIMARY KEY   AUTOINCREMENT,source text, URL text, content text) ") 
        sql = "insert into resultToday (source,URL,content ) values ('Today','"+ url +"','"+ content + "')" 
        sql2 = "DELETE from resultToday where ID NOT IN (Select Max(ID) From resultToday Group By URL)"    #刪除重複的資料      
      
        cursor.execute(sql)
        cursor.execute(sql2)
        connection.commit()  
def todayClimb(pagenum,keyword):
    for i in range(1,pagenum):  #range決定跑幾頁

        #搜尋條件
        key = keyword

        url ='https://www.businesstoday.com.tw/group_search/article?keywords=' + key + '&page='+ str(i) +'&order=new&field=title'
        r = requests.get(url)
        getUrl(r)

    getContent()