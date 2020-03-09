import time
import urllib.parse
from multiprocessing import Pool

import sqlite3

import requests
from bs4 import BeautifulSoup

import re
# from seleniumClimb import getURL

import jieba

keyword = "口罩"
board = 'Lifeismoney'
INDEX = 'https://www.ptt.cc/bbs/'+ board +'/search?q='+ keyword
NOT_EXIST = BeautifulSoup('<a>本文已被刪除</a>', 'lxml').a
content_list = []
contentAssemble = ''

connection = sqlite3.connect('search_Result.db')
cursor = connection.cursor()

def get_posts_list(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    articles = soup.find_all('div', 'r-ent')

    posts = list()
    for article in articles:
        meta = article.find('div', 'title').find('a') or NOT_EXIST
        date = article.find('div', 'date').getText()
        month = int(date[:-3])
        # if month<13 and month>2 :
        #     posts.append({
        #         'title': meta.getText().strip(),
        #         'link': meta.get('href'),
        #         'push': article.find('div', 'nrec').getText(),
        #         'date': article.find('div', 'date').getText(),
        #         'author': article.find('div', 'author').getText(),
        #     })
        posts.append({
            'title': meta.getText().strip(),
            'link': meta.get('href'),
            'push': article.find('div', 'nrec').getText(),
            'date': article.find('div', 'date').getText(),
            'author': article.find('div', 'author').getText(),
            })    
            

    next_link = soup.find('div', 'btn-group-paging').find_all('a', 'btn')[1].get('href')

    return posts, next_link


def get_paged_meta(page):
    page_url = INDEX
    all_posts = list()
    for i in range(page):
        posts, link = get_posts_list(page_url)
        all_posts += posts
        page_url = urllib.parse.urljoin(INDEX, link)
    return all_posts


def get_articles(metadata):
    post_links = [meta['link'] for meta in metadata]
    with Pool(processes=8) as pool:
        contents = pool.map(fetch_article_content, post_links)
        return contents


def fetch_article_content(link):
    url = urllib.parse.urljoin(INDEX, link)
    response = requests.get(url)
    return response.text

def cal(sentence):  #計數丟進CSV
    i = 0 
    hash1 = {}
    word_list = []
    jieba.set_dictionary('dict.txt.big')
    jieba.load_userdict("userdict.txt") #加入自訂文字庫
    # sentence = "獨立音樂需要大家一起來推廣，歡迎加入我們的行列獨立！"
    # print ("Input：", sentence)
    words = jieba.cut(sentence, cut_all=False)
    
    for word in words:
        # print (word)
        #把字加進list
        word_list.append(word)
    for item in word_list:
        if item in hash1 :
            hash1[item] += 1
        else :
            hash1.update({item:1})
    # print (hash1)
    #寫入CSV
    fd = open("count.csv","w",encoding="utf-8")
    fd.write("word,count\n")
    for k in hash1 :
        fd.write("%s,%d\n"%(k,hash1[k]))


if __name__ == '__main__':
    pages = 10
    
    start = time.time()

    metadata = get_paged_meta(pages)
    articles = get_articles(metadata)

    print('花費: %f 秒' % (time.time() - start))

    print('共%d項結果：' % len(articles))
    for post, content in zip(metadata, articles):
        
        wash = '[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
        after1 = re.sub(wash,"",content)
        cleancontent = re.sub('\s','',after1)
        print('{0} {1: <15} {2},  網址:{3}'.format(
            post['date'], post['author'], post['title'],post["link"]))
        content_list.append(cleancontent)
        completelink = "https://www.ptt.cc/" + post['link']
        #要選哪三格不然會跑error
        sql = "insert into resultMoney(source,url,content) values ('PTT','"+ completelink +"','"+ cleancontent + "')"
        cursor.execute(sql)
        connection.commit()
        
    for i in content_list:
        contentAssemble += i
    cal(contentAssemble)