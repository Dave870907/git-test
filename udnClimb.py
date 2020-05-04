import requests
from bs4 import BeautifulSoup
import json
import re
import urllib.parse
import sqlite3




#網址有重複(改好了)
#改好了



url_list = []

#資料庫連線
connection = sqlite3.connect('search_Result.db')
cursor = connection.cursor()

def getURL(r):
    jsontext = r.text

    jsonContent = json.loads(jsontext)
    for i in range(0,20):
        url_list.append(str(jsonContent["lists"][i]["titleLink"]))

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
            
        
            #每個版都不一樣的HTML所以直接找p
            
            article_ps = soup.findAll('p')
            
            
            for p in article_ps:
                if str(p.string) != "None":
                    content+=(str(p.string))
        
        content = content.lstrip() 
        cursor.execute("create table if not exists resultUdn (ID INTEGER PRIMARY KEY   AUTOINCREMENT,source text, URL text, content text) ")   
        sql = "insert into resultUdn (source,URL,content ) values ('Udn','"+ url +"','"+ content + "')" 
        sql2 = "DELETE from resultUdn where ID NOT IN (Select Max(ID) From resultUdn Group By URL)"
        cursor.execute(sql)
        cursor.execute(sql2)
        
        connection.commit()
def udnClimb(pagenum,keyword):
    for i in range(1,pagenum):
        key = keyword
        url = 'https://udn.com/api/more?page='+ str(i) +'&id=search:'+ key +'&channelId=2&type=searchword'
        r = requests.get(url)
        getURL(r) 
        # print(url_list)
        # print(len(url_list))
    getContent()

