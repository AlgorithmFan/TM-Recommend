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
    ItemSet = set()
    for line in reader:
        if reader.line_num==1:
            continue
        user_id = int(line[0])
        item_id = int(line[1])
        behavior = int(line[2])
        geo = line[3]
        item_category = int(line[4])
        timestamp = time.mktime(time.strptime(line[5], formatter))
        if user_id not in UserModels:
            UserModels[user_id] = CUserModel(user_id)
        UserModels[user_id].addItem(item_id, behavior, geo, timestamp)
        ItemSet.add(item_id)

    ItemList = list(ItemSet)

    for user_id in UserModels:
        UserModels[user_id].staticData(ItemList, 'd')
    return UserModels, ItemList

def ReadItemDict(Filename):
    '''读取数据'''
    CsvFile = file(Filename, 'rb')
    reader = csv.reader(CsvFile)
    ItemDict = {}
    for line in reader:
        if reader.line_num==1:
            continue
        item_id = int(line[0])
        item_geohash = line[1]
        item_category = int(line[2])
        ItemDict[item_id] = (item_geohash, item_category)
    return ItemDict


def calRec(recommendation, mUserModels, top_num):
    hitNum, recall, precision = 0, 0, 0
    for user_id in recommendation:
        if mUserModels[user_id].test is None:
            continue
        index = np.nonzero(mUserModels[user_id].test>0)
        recall += len(index[0])
        precision += len(recommendation[user_id][:top_num])
        for item_index in recommendation[user_id][:top_num]:
            if sum(mUserModels[user_id].test[:, item_index])>0:
                hitNum += 1
    return hitNum, recall, precision


if __name__=='__main__':
    filename = r'J:\DataSet\Competition\test.csv'
    columnHeader = ['user_id', 'item_id']
    Data = [(1,1), (1,2)]
    WriteCSV(filename, columnHeader, Data)

    print 'Download Item file.'
    filename = r'J:\DataSet\Competition\train_item.csv'
    mItemDict = ReadItemDict(filename)
    print 'The number of items is %d.' % len(mItemDict)

    print 'Download User file.'
    filename = r'J:\DataSet\Competition\train_user.csv'
    mUserModels, mItemList = ReadUserModels(filename)
    print 'The number of users is %d.' % len(mUserModels)
    print 'The number of items is %d.' % len(mItemList)