# -*- coding: utf-8 -*-
# @Time     : 2018/5/9 16:04
# @Author   : Narata
# @Project  : android_app
# @File     : recommend.py
# @Software : PyCharm

import pymysql
import json

db = pymysql.connect('219.216.65.127', 'root', 'narata', 'android', charset='utf8')
cursor = db.cursor()

with open('result.json', 'r') as fp:
    i = 0
    for data in fp.readlines():
        i += 1
        print(i)
        json_data = json.loads(data.replace('\n', '').replace("'", '"'))
        user_id = json_data['user_id']
        value = json_data['value']
        value_sort = sorted(value, key=lambda a: a['value'], reverse=True)[:10]
        for buf in value_sort:
            busi_id = buf['busi_id']
            recommend_value = buf['value']
            sql = "insert into user_recommend(business_id, user_id, value) values('{}', '{}', {})".format(busi_id, user_id, recommend_value)
            print(sql)
            cursor.execute(sql)
        db.commit()

db.close()
