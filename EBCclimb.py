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
    
    div = soup.find('div',{'class':'realtime white-box news-list-area'})
    if div != None:
        boxes = div.findAll('div',{'class':'style1 white-box'})
    
        for i in boxes:
            link_a = i.find("a")
            href = link_a.get('href')
            url = "https://news.ebc.net.tw/"+href
            url_list.append(url)
    
def getContent():
    #順便寫入資料庫
    
    for url in url_list:
      content = ''
      res = requests.get(url)
      if res.status_code == 200:
          body = res.content
          # 以 Beautiful Soup 解析 HTML 程式碼
          soup = BeautifulSoup(body, "html.parser")
          # 要怎麼得到乾淨的網站內文字
          # 用bs4清理
          
          article = soup.find('div',{'id':'contentb'})
          article_ps = article.findAll('p')
          
          for p in article_ps:
            if str(p.string) != "None":
                content+=(str(p.text))
            
              
      
      cursor.execute("create table if not exists resultEBC (ID INTEGER PRIMARY KEY   AUTOINCREMENT,source text, URL text, content text) ")
      sql = "insert into resultEBC (source,URL,content ) values ('EBC','"+ url +"','"+ content + "')" 
      sql2 = "DELETE from resultEBC where ID NOT IN (Select Max(ID) From resultEBC Group By URL)"    #刪除重複的資料      
      
      cursor.execute(sql)
      cursor.execute(sql2)
      connection.commit()  
def EBCclimb(pagenum,keyword):
    for i in range(0,pagenum):  #range決定跑幾頁

        #搜尋條件
        key = keyword

        url = 'https://news.ebc.net.tw/Search/Result?type=keyword&value='+ key +'&page=' + str(i)
        r = requests.get(url)
        getUrl(r)
    getContent()
# print(url_list)
# print(len(url_list))


