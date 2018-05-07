# -*- coding: utf-8 -*-
# @Time     : 2018/5/6 17:12
# @Author   : Narata
# @Project  : android_app
# @File     : insert_user.py
# @Software : PyCharm


import pymongo
import json

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.android
collection = db.user


def insert():
    with open('../dataset/user.json', 'rb') as fp:
        i = 0
        for data in fp.readlines():
            json_data = json.loads(data)
            result = collection.insert(json_data)
            i += 1
            print(i, result)


if __name__ == '__main__':
    insert()