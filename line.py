import requests
from bs4 import BeautifulSoup
import re
import json
import sqlite3


#連接資料庫
conn = sqlite3.connect('search_Result.db')
cur = conn.cursor()

# # 查看抓下來的內容存到記事本
# def writeText(name, text):
#     with open(name, 'w', encoding='UTF-8') as file:
#         file.write(str(text))

# 抓每個網址的內文
def readUrl(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,"html.parser")
    # print(url)
    # writeText('bbb.txt', soup)


    # 發布時間
    # date = soup.find('p',{'class':'date'}).string
    # print(date)
    #篩選時間

    #抓取文章內容
    article = soup.find('article',{'class':'news-content'})
    ps = article.find_all('p')
    # print(ps)


    content = ''

    # 把tag取代掉

    for p in ps:
        
        # p = str(article).replace('<br/','')
        # p = re.sub(u'\\<.*?\\>','',p)
        content += str(p) + '\n'
        content = str(content).replace('<br/','')
        content = re.sub(u'\\<.*?\\>','',content)
    content = str(content).replace("'","’")

    # print(content)

    #建立/寫入table
    cur.execute("create table if not exists line_result(id integer primary key autoincrement,link text, content text, source text)")
    sql_command = "insert into line_result(link,content,source) values('"+url+"','"+content+"','line新聞')"

    conn.execute(sql_command)
    conn.commit()
    
# keyword ="口罩"

def line(pagenum,keyword):
    # 要爬的url
    for i in range(1,pagenum+1):
        resp = requests.get('https://hub.line.me/search/'+keyword+'?module=news&sort=REL&pageIndex='+str(i))
        #解析當前網頁html
        soup = BeautifulSoup(resp.text,"html.parser")
        div = soup.find("div",{'class':'searchToday-itemsContainer'})
        hrefs = div.find_all("a")
        for href in hrefs:
            # print(href.get('href'))
            readUrl(href.get("href"))
            # break
        # print(hrefs)
        # break
    # print(soup)
    # writeText('aaa.txt', soup)

# line(2,'口罩')






