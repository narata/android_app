# -*- coding: utf-8 -*-
# @Time     : 2018/5/6 19:49
# @Author   : Narata
# @Project  : android_app
# @File     : insert_business.py
# @Software : PyCharm


import pymysql
import json

db = pymysql.connect('localhost', 'root', 'narata', 'android', charset='utf8')
cursor = db.cursor()

with open('../dataset/business.json', 'rb') as fp:
    i = 0
    for data in fp.readlines():
        json_data = json.loads(data)
        cursor.execute(
            "insert into user_business(id, name, star, attribute, comment_count) values('{}', '{}', {}, '', {})"
            .format(json_data['business_id'], pymysql.escape_string(json_data['name']), json_data['stars'],json_data['review_count']))
        i += 1
        if i % 100 == 0:
            db.commit()
        print(i)

db.commit()
db.close()
