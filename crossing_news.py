#換日線
import re
import requests
from bs4 import BeautifulSoup
import sqlite3
import json

#連接資料庫
conn = sqlite3.connect('search_Result.db')
cur = conn.cursor()

def readUrl(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,'html.parser')
    # spans = soup.find('div',{'class':'article-info'})
    # info = spans.find('span')
    # print(url,info.string)
    # print(url)
    article = soup.find('div',{'class':'trackSection'})
    content = ''
    if article != None:
        ps = article.find_all('p')
        for p in ps:
            if not(p.string is None):
                content += str(p.string) + '\n'
    
    else:
        pass
    # print(content)
    

    #建立/寫入table
    cur.execute("create table if not exists crossingNews_result(id integer primary key autoincrement,link text, content text, source text)")
    sql_command = "insert into crossingNews_result(link,content,source) values('"+url+"','"+content+"',' 換日線')"

    conn.execute(sql_command)
    conn.commit()
    


# keyword = '口罩'
# #不能寫死
# pageNum = 25

def crossing_news(pagenum,keyword):

    for i in range(1,pagenum+1):
        resp = requests.get('https://crossing.cw.com.tw/blogSearch.action?key='+keyword+'&page='+str(i))
        soup = BeautifulSoup(resp.text,"html.parser")
        article = soup.find('div',{'class':'card-group card-grid'})  
        hrefs = list(article.find_all('a'))
        hrefs = hrefs[::6]
        
     
       
        for href in hrefs:
            # readUrl(href.get('href'))
            href = href.get('href')
            # print(href)
            readUrl(href)
            # break
        

        # break

# crossing_news(2,'口罩')