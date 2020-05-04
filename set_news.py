#三立新聞
import re
import requests
from bs4 import BeautifulSoup
import sqlite3
import json


#連接資料庫
conn = sqlite3.connect("search_Result.db")
cur = conn.cursor()

#寫進file查看
# def writeText(name, text):
#     with open(name, 'w', encoding='UTF-8') as file:
#         file.write(str(text))

def readUrl(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,'html.parser')
    info = soup.find('div',{'class':'page-title-text'})
    date = info.find('time')
    # print(url,date.string)

    

    article = soup.find('div',{'id':'Content1'})
    ps = article.find_all('p')
#     writeText('cw.txt',ps)
    content = ''
    for p in ps:
        p = str(p).replace('<br/','')
        p = re.sub(u'\\<.*?\\>','',p)
#         if not(p.string is None):
        content += str(p) + '\n'

    content = str(content).replace("'","’")
    # print(content)
    
    #建立/寫入table
    cur.execute("create table if not exists setNews_result (ID INTEGER PRIMARY KEY   AUTOINCREMENT,link text,content text,source text) ")
    sql_command = "insert into setNews_result(link,content,source) values('"+url+ "','" + content + "', '三立')"

    conn.execute(sql_command)
    conn.commit()

keyword = '口罩'
#不能寫死
pageNum = 25
# resultList = []
def set_news(pagenum,keyword):
    for i in range(1,pageNum+1):
        resp = requests.get('https://www.setn.com/search.aspx?q='+keyword+'&p='+str(i))
        soup = BeautifulSoup(resp.text,"html.parser")
        article = soup.find('div',{'class':'container main-news-area'}) 
        # divs = article.findAll('div',{'class':'col-lg-4 col-sm-6'}) 
        hrefs = article.find_all('a') 
        # print(hrefs)
        
        for href in hrefs:
            # result = readUrl(href.get('href'))
            result = href.get('href')
            
            if 'News' in result and '口罩' in result:
                # resultList.append('https://www.setn.com/'+result)
                # a = resultList[::2]
                # for i in a:
                #     readUrl(i)
                readUrl('https://www.setn.com/'+result)
                # break
            # readUrl(href)
            
        break
    #存入資料庫

# set_news(2,'口罩')