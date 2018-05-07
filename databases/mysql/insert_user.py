# -*- coding: utf-8 -*-
# @Time     : 2018/5/6 20:21
# @Author   : Narata
# @Project  : android_app
# @File     : insert_user.py
# @Software : PyCharm


import pymysql
import json
import time

db = pymysql.connect('localhost', 'root', 'narata', 'android', charset='utf8')
cursor = db.cursor()

with open('../dataset/user.json', 'rb') as fp:
    i = 2
    for data in fp.readlines():
        json_data = json.loads(data)
        try:
            cursor.execute(
                "insert into auth_user(id, password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) values({}, '{}', 0, '{}', '{}', '{}', '', 0, 1, '{}')"
                .format(i, 'pbkdf2_sha256$30000$MgcnPfgN75mc$ikQz2STvxA99oiVVitVoiGGJGDLclK0BqKVPJWogAjg=', json_data['user_id'], pymysql.escape_string(json_data['name']), pymysql.escape_string(json_data['name']), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            cursor.execute(
                "insert into user_user(id, user_id, average_stars, comment_count) values('{}', {}, {}, {})"
                .format(json_data['user_id'], i, json_data['average_stars'], json_data['review_count'])
            )
        except pymysql.err.DataError:
            cursor.execute(
                "insert into auth_user(id, password, is_superuser, username, first_name, last_name, email, is_staff, "
                "is_active, date_joined) values({}, '{}', 0, '{}', '{}', '{}', '', 0, 1, '{}')"
                    .format(i, 'pbkdf2_sha256$30000$MgcnPfgN75mc$ikQz2STvxA99oiVVitVoiGGJGDLclK0B qKVPJWogAjg=',
                            json_data['user_id'], '', '',
                            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            cursor.execute(
                "insert into user_user(id, user_id, average_stars, comment_count) values('{}', {}, {}, {})"
                    .format(json_data['user_id'], i, json_data['average_stars'], json_data['review_count'])
            )
        i += 1
        if i % 100 == 0:
            db.commit()
        print(i)
        

db.commit()
db.close()