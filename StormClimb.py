import requests
from bs4 import BeautifulSoup
#改完了
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
    div = soup.findAll('div',{'class':'category_card card_thumbs_left'})
    
    for i in div:
        link_a = i.find("a",{"class":"card_link link_title"})
        href = link_a.get('href')
        url = "https://www.storm.mg/"+href
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
          
          article = soup.find('article')
          article_ps = article.findAll('p')
          
          for p in article_ps:
            if str(p.string) != "None":
                content+=(str(p.text))
            
              
      cursor.execute("create table if not exists resultStorm (ID INTEGER PRIMARY KEY   AUTOINCREMENT,source text, URL text, content text) ")
      sql = "insert into resultStorm (source,URL,content ) values ('StormMedia','"+ url +"','"+ content + "')" 
      sql2 = "DELETE from resultStorm where ID NOT IN (Select Max(ID) From resultStorm Group By URL)"    #刪除重複的資料      
      
      cursor.execute(sql)
      cursor.execute(sql2)
      connection.commit()  
def stormClimb(pagenum,keyword):
    for i in range(1,pagenum):  #range決定跑幾頁

        #搜尋條件
        key = keyword

        url = 'https://www.storm.mg/site-search/result/' + str(i) + '?q=' + key
        r = requests.get(url)
        getUrl(r)
    # print(url_list)
    # print(len(url_list))
    getContent()
# stormClimb(2,'口罩')