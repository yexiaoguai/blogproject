#!/usr/bin/env python
#coding:utf-8

import sqlite3

conn = sqlite3.connect("db.sqlite3")
conn.text_factory = str
cur = conn.cursor()

# movies = [





# ]

# cur.executemany("insert into movie_movie values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", movies)

cur.execute("update movie_movie set download_link='magnet:?xt=urn:btih:124276cddc9a729bfd2953105aad4736dd0a472a' where movie_name='保姆日记'")
cur.execute("update movie_movie set download_link='magnet:?xt=urn:btih:af9e39a1c97d7336ae04e39a415f68da974ff433' where movie_name='帕特森'")
cur.execute("update movie_movie set download_link='magnet:?xt=urn:btih:6f5496d40478b2862cd5255155de92026f177f08' where movie_name='大都会'")
cur.execute("update movie_movie set download_link='magnet:?xt=urn:btih:d236e2697bb5b0582210824809e921ac71241719' where movie_name='回到那年夏天'")
cur.execute("update movie_movie set download_link='magnet:?xt=urn:btih:cd2ee68f61588b983d4b468e7eafc9cd1d0ad3b2' where movie_name='风口青春'")
cur.execute("update movie_movie set download_link='magnet:?xt=urn:btih:2df256be4905bc9b1430631f9a357a82473cf2e7' where movie_name='我为相亲狂'")
cur.execute("update movie_movie set download_link='magnet:?xt=urn:btih:500a13b54ae15ef6bf1df50ad568eeb22dc103da' where movie_name='啊朋友还钱'")
cur.execute("update movie_movie set download_link='magnet:?xt=urn:btih:32293f1dee5f14ce91180e2fbc6b2d640f07f787' where movie_name='蓝色情人节'")
cur.execute("update movie_movie set download_link='magnet:?xt=urn:btih:CB0174F3F63C5B0C47A4CD456633909DA2261A45' where movie_name='金融决战'")
cur.execute("update movie_movie set download_link='magnet:?xt=urn:btih:fcfdab7c5adb4cacd7fdd5bbabe55b871baf7269' where movie_name='反贪风暴2'")
cur.execute("update movie_movie set download_link='magnet:?xt=urn:btih:2a5e74ed8e64d6449f9138d63b1fc23e7517e7cd' where movie_name='新世界'")
cur.execute("update movie_movie set download_link='magnet:?xt=urn:btih:f315ef31e21beaa485f05767a9be0d282732d0be' where movie_name='我不是你的黑鬼'")
cur.execute("update movie_movie set download_link='magnet:?xt=urn:btih:A908A65291519C7985FFD6FB9F36EB24DAE2DCE7' where movie_name='变形金刚5：最后的骑士'")

conn.commit()