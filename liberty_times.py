import requests
from bs4 import BeautifulSoup
import re
import json
import sqlite3

#連接資料庫
conn = sqlite3.connect('search_Result.db')
cur = conn.cursor()


# def writeText(name, text):
#     with open(name, 'w', encoding='UTF-8') as file:
#         file.write(str(text))


def readUrl(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,'html.parser')
    # writeText('ccc.txt',soup)
    # print(url)
    article = soup.find('div',{'class':'text boxTitle boxText'})
    content = ''
    if article != None:
        ps = article.find_all('p')
        for p in ps:
            content += str(p.string) +'\n'
    else:
        pass
    content = str(content).replace("'", "’")
    # print(content,url)
      
    #建立/寫入table
    cur.execute("create table if not exists libertyTimes_result(id integer primary key autoincrement,link text, content text, source text)")
    sql_command = "insert into libertyTimes_result(link,content,source) values('"+url+"','"+content+"','自由時報')"

    conn.execute(sql_command)
    conn.commit()
    




# # keyword = input("請輸入關鍵字:")
# keyword = "口罩"
# pageNum = 396

def liberty_times(pageNum,keyword):
    startTime = "2019-12-10"
    endTime = "2020-03-09"
    for i in range(1,pageNum):
        resp = requests.get("https://news.ltn.com.tw/search?keyword="+keyword+"&start_time="+startTime+"&end_time="+endTime+"&page="+str(pageNum))
        soup = BeautifulSoup(resp.text,"html.parser")
        # writeText('ccc.txt',soup)
        div = soup.find('ul',{'class':'searchlist boxTitle'})
        hrefs = div.find_all('a')
        for href in hrefs:
            href = href.get("href")
            readUrl(href)
            # break
            # print(href)
        # h2s = soup.find_all("h2")
        # for h2 in h2s:
        #     print(h2)
        # break

# liberty_times(4,'口罩')