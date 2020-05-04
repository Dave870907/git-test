
#三立新聞
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
    info = soup.find('section',{'class':'article_head'})
    date = info.find('time')
    # print(url,date.string)

    article = soup.find('div',{'calss':'article_text'})

    content = ''
    for p in article:
        p = str(article).replace('<br/','')
        p = re.sub(u'\\<.*?\\>','',p)
        content += str(p) + '\n'
    content = str(content).replace("'","’")
    # print(content)

    #建立/寫入table
    cur.execute("create table if not exists pchome_result(id integer primary key autoincrement,link text, content text, source text)")
    sql_command = "insert into pchome_result(link,content,source) values('"+url+"','"+content+"','pchome')"

    conn.execute(sql_command)
    conn.commit()
    


def pchome(pagenum,keyword):
    resultList = []
    for i in range(1,pagenum+1):
        resp = requests.get('https://news.pchome.com.tw/search.php?k='+keyword+'&submit=Go&p='+str(i))
        soup = BeautifulSoup(resp.text,"html.parser")
        article = soup.find('div',{'class':'contbar'})  
        hrefs = article.find_all('a') 
        # print(hrefs)
        
        for href in hrefs:
            result = href.get('href')
            
            
            
            if 'index' in result :
                resultList.append('https://news.pchome.com.tw/'+result)
        
                a = resultList[::3]
        # print(a)
        for i in a:
            readUrl(i)
        # break
            
        

        break

# pchome(2,'口罩')