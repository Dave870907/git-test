import sqlite3
connection = sqlite3.connect("search_Result.db")
cursor = connection.cursor()
#autoincrement 自動生成編號
cursor.execute("create table if not exists resultMoney (ID INTEGER PRIMARY KEY   AUTOINCREMENT,source text, URL text, content text) ")
cursor.execute("create table if not exists resultGossip (ID INTEGER PRIMARY KEY   AUTOINCREMENT,source text, URL text, content text) ")
cursor.execute("create table if not exists resultyahoo (ID INTEGER PRIMARY KEY   AUTOINCREMENT,source text, URL text, content text) ")
