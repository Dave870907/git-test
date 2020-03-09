import requests
from bs4 import BeautifulSoup
import json
import re
import urllib.parse
import sqlite3

#list
sumList = []
titleList = []
urlList = []
content_list = []
content_list2 = []

#搜尋條件
keyword = "口罩"
offset = 0

#資料庫連線
connection = sqlite3.connect('search_Result.db')
cursor = connection.cursor()

def getContent():
    #順便寫入資料庫
    
    for url in urlList:
      content = ''
      res = requests.get(url)
      if res.status_code == 200:
          body = res.content
          soup = BeautifulSoup(body, "html.parser")
          # 要怎麼得到乾淨的網站內文字
          # 用bs4清理
          article = soup.find('article')
          article_ps = article.findAll('p')
          for p in article_ps:
            if str(p.string) != "None":
              content+=(str(p.string))

      sql = "insert into resultyahoo (source,URL,content ) values ('yahoo','"+ url +"','"+ content + "')" 
      cursor.execute(sql)
      connection.commit()
      
      # break

    

    # for i in content_list:  #清理多餘的英文字
    #     r1 = '[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
    #     string1 = re.sub(r1,"",i)
    #     string2 = re.sub("\s",'',string1)
    #     content_list2.append(string2)
    # print(content_list2)

def getURL(r): 
  jsontext = r.text

  jsonContent = json.loads(jsontext)

  for i in range(0,10):
    before = str(jsonContent["data"][i]['url'])
    changed = urllib.parse.unquote(before)
    theUrl = "https://tw.news.yahoo.com/"+ changed
    urlList.append(theUrl)

def gettitle(r):
  jsontext = r.text

  jsonContent = json.loads(jsontext)

  for i in range(0,10):
    titleList.append(str(jsonContent["data"][i]['title'])) 

def getSummary(r):
  jsontext = r.text

  jsonContent = json.loads(jsontext)

  for i in range(0,10):
    sumList.append(str(jsonContent["data"][i]['summary']))

for i in range(0,2):
  url = 'https://tw.news.yahoo.com/_td-news/api/resource/NewsSearchService;loadMore=true;mrs=%7B%22size%22%3A%7B%22w%22%3A220%2C%22h%22%3A128%7D%7D;offset='+ str(offset) +';query='+ keyword +';usePrefetch=false?bkt=news-TW-zh-Hant-TW-def&device=desktop&feature=videoDocking&intl=tw&lang=zh-Hant-TW&partner=none&prid=52d6sotf613pr&region=TW&site=news&tz=Asia%2FTaipei&ver=2.3.1371&returnMeta=true'
  r = requests.get(url)
  getURL(r) 
  # gettitle(r)
  # getSummary(r)
  offset += 10
# print(urlList)
# print(sumList)
# print(titleList)  
# print(len(urlList))
# print(len(titleList))
# print(len(sumList))
getContent()