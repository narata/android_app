# -*- coding: utf-8 -*-
# @Time     : 2018/5/6 20:21
# @Author   : Narata
# @Project  : android_app
# @File     : insert_comment.py
# @Software : PyCharm


import pymysql
import json

db = pymysql.connect('localhost', 'root', 'narata', 'android', charset='utf8')
cursor = db.cursor()

with open('../dataset/review.json', 'rb') as fp:
    i = 0
    for data in fp.readlines():
        json_data = json.loads(data)
        cursor.execute(
            "insert into user_comment(id, date, text, star, business_id, user_id) "
            "values('{}', '{}', '{}', {}, '{}', '{}')"
            .format(json_data['review_id'], json_data['date'], pymysql.escape_string(json_data['text']),
                    json_data['stars'], json_data['business_id'], json_data['user_id']))
        i += 1
        if i % 100 == 0:
            db.commit()
        print(i)

db.commit()
db.close()