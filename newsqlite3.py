#!/usr/bin/env python
#coding:utf-8

import sqlite3

conn = sqlite3.connect("db.sqlite3")
conn.text_factory = str
cur = conn.cursor()

movies = [



]

cur.executemany("insert into movie_movie values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", movies)




conn.commit()