import requests
from bs4 import BeautifulSoup
import json
import re
import urllib.parse
import sqlite3

url_list = []

#資料庫連線
connection = sqlite3.connect('search_Result.db')
cursor = connection.cursor()



def getUrl(r) :
    content = r.content
    soup = BeautifulSoup(content, "html.parser")
    
    div = soup.findAll("div",{"class":"archive clearfix"})
    for i in div:
        href = i.findAll('a')
        # print(href)
        for j in href:
            url = j.get('href')
            url_list.append(url)
            break


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
          article_div = article.find('div',{'class':'story'})
          article_ps = article_div.findAll('p')
          for p in article_ps:
            if str(p.find('span'))!= 'None':
                strong = p.find('span')           
                content += (str(strong.string))
          
          for p in article_ps:
            if str(p.string) != "None":
                content+=(str(p.text))
            
              

      sql = "insert into resultETtoday (source,URL,content ) values ('ETtoday','"+ url +"','"+ content + "')" 
      cursor.execute(sql)
      connection.commit()  

for i in range(0,2):  #range決定跑幾頁
    
    #搜尋條件
    keyword = "口罩"

    url = 'https://www.ettoday.net/news_search/doSearch.php?keywords='+ keyword +'&idx=1&page='+ str(i+1)
    r = requests.get(url)
    getUrl(r)
print(url_list)
print(len(url_list))
getContent()