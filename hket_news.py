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
   
    # print(url)
    article = soup.find('div',{'class':'article-detail-content-container'})
    # ps = article.find_all('p')
    content = ''
    if article != None:
        ps = article.find_all('p')
        for p in ps:
            if not(p.string is None):
                content += str(p.string) + '\n'
    
    else:
        pass

    # print(content)
    # for p in ps:
    #     if not(p.string is None):
    #         content += str(p.string) + '\n'
    # print(content)

    #建立/寫入table
    cur.execute("create table if not exists hketNews_result(id integer primary key autoincrement,link text, content text, source text)")
    sql_command = "insert into hketNews_result(link,content,source) values('"+url+"','"+content+"','香港經濟日報')"

    conn.execute(sql_command)
    conn.commit()
    


# keyword = '口罩'
# pageNum = 25

def hket_news(pagenum,keyword):
    for i in range(1,pagenum):
        resp = requests.get('https://service.hket.com/search/result?dis=basic&keyword='+keyword+'&p='+str(i))
        soup = BeautifulSoup(resp.text,"html.parser")
        article = soup.find('div',{'class':'template-default hket-row no-space main-listing-container'})  
        hrefs = article.find_all('a')[::2]
        # print(hrefs)
        for href in hrefs:
            # print(href.get('href'))
            readUrl(href.get('href'))
            # break
        

        # break

hket_news(2,'口罩')



