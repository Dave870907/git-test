import requests
from bs4 import BeautifulSoup
import re
import json
import sqlite3

#建資料庫
conn = sqlite3.connect("search_Result.db")
cur = conn.cursor()


# cur.execute('create table dcard_result (id integer primary key autoincrement, link, content, source)')
# cur.execute('create table dcard_comment (id integer primary key autoincrement , comment)')

def dcard(keyword):
    # keyword = input("請輸入關鍵字:")
    # keyword ="寶雅福袋"

    #要爬的url
    resp = requests.get('https://www.dcard.tw/search?query='+keyword)

    #解析當前網頁html
    soup = BeautifulSoup(resp.text,"html.parser")


    #找出當前網頁所有文章id
    h2s = soup.find_all("h2")
    urlnum = []
    for i in h2s:
        urlnum.append(i.a.get("href").split('/')[-1])
    # print(urlnum)

    #將文章內容及留言抓下來
    contents = []
    comments = []
    while urlnum:
        #爬每一篇文章內文
        url = "http://dcard.tw/_api/posts/" + str(urlnum[0])
        dcard_api = requests.get(url)
        api_html = BeautifulSoup(dcard_api.text,"html.parser")
        #只抓取'content'的內容
        content = json.loads(str(api_html))['content']

        #爬每一篇文章留言
        dcard_comment = requests.get('http://dcard.tw/_api/posts/'+ str(urlnum[0])+'/comments')
        comment_html = BeautifulSoup(dcard_comment.text,"html.parser")
        
        # contents.append(json.loads(str(api_html)))
        # conn.execute('insert into dcard_result values' + json.loads(str(api))['content'])
        # comments.append(json.loads(str(comment_html)))
        d = json.loads(str(comment_html))
        for j in range(0,len(d)):
            try:
                #只抓取'content'的內容
                comment = d[j]['content']
                #存入資料庫str(urlnum[0])
                cur.execute("create table if not exists dcard_comment (ID INTEGER PRIMARY KEY   AUTOINCREMENT,comment text) ")
                sql_command = "insert into dcard_comment(comment) values('"  + comment +"')"
                # print(sql_command)
                conn.execute(sql_command)
                conn.commit()
                # print(comment)
            except:
                pass
        #存入資料庫
        cur.execute("create table if not exists dcard_result (ID INTEGER PRIMARY KEY   AUTOINCREMENT,link text,content text,source text) ")
        sql_command = "insert into dcard_result(link,content,source) values('"+url+ "','" + content + "', 'dcard')"
    
        conn.execute(sql_command)
        
        
        # print(sql_command)
    
        urlnum.pop(0)
    conn.commit()

# dcard('口罩')


#抓取想要的部分
# print(type(content[0]))
# for i in contents:
#     print(i['content'])
#     print('---------------我是分隔號---------------')

# for i in comments:
#     # print(i[0]['content'])
#     for j in range(0,len(i)):
#         try:
#             print(i[j]['content'])
#         except:
#             pass
#         print('---------------我是分隔號',j,'---------------')
#     print('---------------結束---------------')







