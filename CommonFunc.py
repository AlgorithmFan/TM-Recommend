#!usr/bin/env python
#coding:utf-8

import csv
import time
from UserModel_1 import CUserModel
import numpy as np

def WriteCSV(Filename, ColumnHeader, Data):
    '''写入文件'''
    CsvFile = file(Filename, 'wb')
    Writer = csv.writer(CsvFile)
    Writer.writerow(ColumnHeader)
    Writer.writerows(Data)
    CsvFile.close()

def ReadUserModels(Filename):
    '''读取数据'''
    formatter = '%Y-%m-%d %H'
    CsvFile = file(Filename, 'rb')
    reader = csv.reader(CsvFile)
    UserModels = {}
    ItemCategory = {}
    for line in reader:
        if reader.line_num==1:
            continue
        user_id = int(line[0])
        item_id = int(line[1])
        behavior = int(line[2])
        geo = line[3]
        item_category = int(line[4])
        timestamp = int(time.mktime(time.strptime(line[5], formatter)))
        if user_id not in UserModels:
            UserModels[user_id] = CUserModel(user_id)
        UserModels[user_id].addItem(item_id, behavior, geo, timestamp)
        ItemCategory[item_id] = item_category

    return UserModels, ItemCategory

def calRec(recommendation, mUserModels, top_num):
    hitNum, recall, precision = 0, 0, 0
    for user_id in recommendation:
        if mUserModels[user_id].test is None:
            continue
        recall += len(mUserModels[user_id].test)
        precision += len(recommendation[user_id][:top_num])
        hitNum += len(mUserModels[user_id].test & set(recommendation[user_id][:top_num]))
    return hitNum, recall, precision

def ReadData(filename, lastStamp, num=10000):
    '''读取数据'''
    formatter = '%Y-%m-%d %H'
    csvFile = file(filename, 'rb')
    reader = csv.reader(csvFile)
    userItems = {}
    ItemCategory = {}
    for line in reader:
        if reader.line_num == 1:
            continue
        # elif reader.line_num == num:
        #     break
        user_id = int(line[0])
        item_id = int(line[1])
        behavior = int(line[2])
        geo = line[3]
        item_category = int(line[4])
        timestamp = int(time.mktime(time.strptime(line[5], formatter)))
        if timestamp >= lastStamp:  continue
        userItems.setdefault(user_id, dict())
        userItems[user_id].setdefault(item_id, [])
        userItems[user_id][item_id].append((behavior, geo, timestamp))
        ItemCategory[item_id] = item_category

    return userItems, ItemCategory
