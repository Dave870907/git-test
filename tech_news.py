#https://technews.tw/page/3/?s=口罩
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
    spans = soup.find_all('span', {'class','body'})
    # time = spans.find('span')
    # info = spans.find_next_sibling()
    # print(url,info.string)
    date = spans[1].string
    # print(url,date)
    article = soup.find('div',{'class':'indent'})
    ps = article.find_all('p')
    content = ''
    for p in ps:
        if not(p.string is None):
            content += str(p.string) + '\n'
    # print(content)
    #建立/寫入table
    cur.execute("create table if not exists techNews_result(id integer primary key autoincrement,link text, content text, source text)")
    sql_command = "insert into techNews_result(link,content,source) values('"+url+"','"+content+"','科技新報')"

    conn.execute(sql_command)
    conn.commit()    


# keyword = '口罩'
# pageNum = 25

def tech_news(pageNum,keyword):
    for i in range(1,pageNum+1):
        resp = requests.get('https://technews.tw/page/'+str(i)+'/?s='+keyword)
        soup = BeautifulSoup(resp.text,"html.parser")
        article = soup.find('section',{'class':'site-content'})  
        hrefs = article.find_all('a') 
        # info = article.find_all('span',{'class':'body'})
        # print(hrefs)
    
        for href in hrefs:
            # url = href.get('href')
            # date = info.string
            # print(url,date)
            href = href.get('href')
            if '/2020/' in href or '/2019/' in href:
                # href.split('/')
                readUrl(href)
                # break
        
        

        # break

# tech_news(2,'口罩')