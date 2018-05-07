# -*- coding: utf-8 -*-
# @Time     : 2018/5/6 16:55
# @Author   : Narata
# @Project  : android_app
# @File     : insert_comment.py
# @Software : PyCharm

import pymongo
import json

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.android
collection = db.comment


def insert():
    with open('../dataset/review.json', 'rb') as fp:
        i = 0
        for data in fp.readlines():
            json_data = json.loads(data)
            result = collection.insert(json_data)
            i += 1
            print(i, result)


if __name__ == '__main__':
    insert()