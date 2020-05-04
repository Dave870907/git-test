#天下雜誌
import re
import requests
from bs4 import BeautifulSoup
import sqlite3
import json

#連接資料庫
conn = sqlite3.connect('search_Result.db')
cur = conn.cursor()

# def writeText(name, text):
#     with open(name, 'w', encoding='UTF-8') as file:
#         file.write(str(text))

def readUrl(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,'html.parser')
    # spans = soup.find('address',{'class':'authorInfor'})
    # info = spans.find('time')
    # print(url,info.string)
    # print(url)

    

    article = soup.find('div',{'class':'main'})
    ps = article.find_all('p')
    # writeText('cw.txt',ps)
    content = ''
    for p in ps:
        p = str(p).replace('<br/','')
        p = re.sub(u'\\<.*?\\>','',p)
#         if not(p.string is None):
        content += str(p) + '\n'
    content = str(content).replace("'", "’")
    # print(content)

    #建立/寫入table
    cur.execute("create table if not exists CW_result(id integer primary key autoincrement,link text, content text, source text)")
    sql_command = "insert into CW_result(link,content,source) values('"+url+"','"+content+"','天下雜誌')"

    conn.execute(sql_command)
    conn.commit()
    


# keyword = '口罩'
# #不能寫死
# pageNum = 25
def CW(pagenum,keyword):
    for i in range(1,pagenum+1):
        resp = requests.get('https://www.cw.com.tw/search/doSearch.action?key='+keyword+'&channel=all&sort=related&page='+str(i))
        soup = BeautifulSoup(resp.text,"html.parser")
        article = soup.find('div',{'class':'articleGroup'})  
        hrefs = article.find_all('a')[::3]
        # print(hrefs)
        for href in hrefs:
            # print(href.get('href'))
            readUrl(href.get('href'))
            # href = str(href.get('href')).replace('&amp','')
            # readUrl(href)
            # break
        

        # break
# CW(2,'口罩')