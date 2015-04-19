#!usr/bin/env python
#coding:utf-8
from ReadConf import CReadConfig
from CommonFunc import ReadUserModels, WriteCSV
import csv


def StaticPopular(Filename, Result_Filename):
    UserModels, ItemCategory = ReadUserModels(Filename)
    PopularNum = {}

    for user_id in UserModels:
        for item_id, behavior, user_geohash, timestamp in UserModels[user_id].Items:
            if item_id not in PopularNum:
                PopularNum[item_id] = [0, 0, 0, 0]
            PopularNum[item_id][behavior-1] += 1

    Data = [(item_id, PopularNum[item_id][0], PopularNum[item_id][1],
             PopularNum[item_id][2], PopularNum[item_id][3]) for item_id in PopularNum]
    WriteCSV(Result_Filename, ['item_id', 'click', 'favorite', 'cart', 'buy'], Data)

def ReadPopular(Filename, Result_Filename):
    '''读取数据'''
    formatter = '%Y-%m-%d %H'
    CsvFile = file(Filename, 'rb')
    reader = csv.reader(CsvFile)
    PopularNum = {}
    for line in reader:
        if reader.line_num==1:
            continue
        item_id = int(line[0])
        click = int(line[1])
        favorite = int(line[2])
        cart = int(line[3])
        buy = int(line[4])
        PopularNum[item_id] = [click, favorite, cart, buy]
    PopularNum = sorted(PopularNum.iteritems(), key=lambda x:x[1][3], reverse=True)
    Data = [(item_id, c, f, t, b) for item_id, (c, f, t, b) in PopularNum]
    WriteCSV(Result_Filename, ['item_id', 'click', 'favorite', 'cart', 'buy'], Data)



if __name__ == '__main__':
    mCConfig = CReadConfig("config.ini")
    parameters = mCConfig.getBasic()
    filename = parameters['filename']
    result_filename = 'popular.csv'
    # StaticPopular(filename, result_filename)
    ReadPopular(result_filename, 'popular1.csv')