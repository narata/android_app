# -*- coding: utf-8 -*-
# @Time     : 2018/5/6 20:16
# @Author   : Narata
# @Project  : android_app
# @File     : insert_photos.py
# @Software : PyCharm


import pymysql
import json

db = pymysql.connect('localhost', 'root', 'narata', 'android', charset='utf8')
cursor = db.cursor()

with open('../dataset/photos.json', 'rb') as fp:
    i = 0
    for data in fp.readlines():
        json_data = json.loads(data)
        cursor.execute(
            "insert into user_photo(id, img_url, caption, label, business_id) values('{}', '', '{}', '{}', '{}')"
            .format(json_data['photo_id'], pymysql.escape_string(json_data['caption']), json_data['label'], json_data['business_id']))
        i += 1
        if i % 100 == 0:
            db.commit()
        print(i)

db.commit()
db.close()