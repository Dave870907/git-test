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
    link_a = soup.findAll('a',{'class':'faux-block-link__overlay-link'})
    
    for i in link_a:
        
        url = i.get('href')
        url_list.append(url)
    
def getContent():
    #順便寫入資料庫
    
    for url in url_list:
      content = ''
      trash = '分享平台FacebookMessengerMessengerTwitter人人網開心網微博QQPlurk豆瓣LinkedInWhatsApp複製鏈接這是外部鏈接，瀏覽器將打開另一個窗口'
      res = requests.get(url)
      if res.status_code == 200:
          body = res.content
          soup = BeautifulSoup(body, "html.parser")
          # 要怎麼得到乾淨的網站內文字
          # 用bs4清理
          
          article = soup.find('div',{'class':'story-body'})
          
          article_ps = article.findAll('p')
          
          for p in article_ps:
            if str(p.string) != "None":
                content+=(str(p.string))
            
              
      
      content = content.replace(trash,'')
      cursor.execute("create table if not exists resultBBCnews (ID INTEGER PRIMARY KEY   AUTOINCREMENT,source text, URL text, content text) ")
      sql = "insert into resultBBCnews (source,URL,content ) values ('BBCnews','"+ url +"','"+ content + "')" 
      sql2 = "DELETE from resultBBCnews where ID NOT IN (Select Max(ID) From resultBBCnews Group By URL)"    #刪除重複的資料      
      
      cursor.execute(sql)
      cursor.execute(sql2)
      connection.commit()  
def BBCclimb(pagenum,keyword):
    for i in range(0,pagenum):  #range決定跑幾頁

        #搜尋條件
        key = keyword

        url = 'https://www.bbc.com/zhongwen/trad/search?q=' + key + '&start=' + str(i*10+1)
        r = requests.get(url)
        getUrl(r)
    # print(url_list)
    # print(len(url_list))
    getContent()