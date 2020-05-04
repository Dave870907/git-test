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
    
    h3 = soup.findAll("h3",{"class":"title"})
    for i in h3:
        href = i.find('a')
        url = href.get('href')
        url_list.append(url)

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
          
          article_div = soup.find('div',{'class':'article-body'})
          article_ps = article_div.findAll('p')
          
          for p in article_ps:
            if str(p.string) != "None":
                content+=(str(p.text))
            
              
      cursor.execute("create table if not exists resultChinaTime (ID INTEGER PRIMARY KEY   AUTOINCREMENT,source text, URL text, content text) ")
      sql = "insert into resultChinaTime (source,URL,content ) values ('ChinaTime','"+ url +"','"+ content + "')"  #寫入資料
      sql2 = "DELETE from resultChinaTime where ID NOT IN (Select Max(ID) From resultChinatime Group By URL)"    #刪除重複的資料      
      cursor.execute(sql)
      cursor.execute(sql2)
      connection.commit()  
def chinatimeClimb(pagenum,keyword):
    for i in range(0,pagenum):  #range決定跑幾頁

        #搜尋條件
        key = keyword

        url = 'https://www.chinatimes.com/search/'+ key +'?page='+ str(i) + '&chdtv'
        r = requests.get(url)
        getUrl(r)
    # print(url_list)
    # print(len(url_list))
    getContent()
# chinatimeClimb(2,'口罩')