#!usr/bin/env python
#coding:utf-8

from ReadConf import CReadConfig
from CommonFunc import ReadUserModels, WriteCSV, calRec
import csv
import time

def recommend(UserModel, startstamp, endstamp, top_num, PopularItems):
    recommendation = {}

    for item_id, behavior, user_geohash, timestamp in UserModel.train:
        if item_id not in recommendation:
            recommendation[item_id] = 0
        recommendation[item_id] += 3600.0/(endstamp-timestamp)
    temp = sorted(recommendation.iteritems(), key=lambda x:x[1], reverse=True)
    recommendation = [item_id for item_id, sim in temp if item_id in PopularItems]
    return recommendation[:top_num]

def ReadUserItemStamp(filename):
    pass

def main(Filename):
    PopularItems = {}
    isRec_start = time.mktime(time.strptime('2014-12-18 0', '%Y-%m-%d %H'))
    isRec_end = time.mktime(time.strptime('2014-12-19', '%Y-%m-%d'))
    UserModels, ItemCategory = ReadUserModels(Filename)
    for user_id in UserModels:
        UserModels[user_id].splitDataByDay(isRec_start, isRec_end)
        UserModels[user_id].isRecommend(isRec_start, isRec_end)
        Items = UserModels[user_id].getBuyItems(isRec_end)
        for item_id in Items:
            if item_id not in PopularItems:
                PopularItems[item_id] = 0
            PopularItems[item_id] += 1

    recommendation = {}
    for user_id in UserModels:
        if UserModels[user_id].isRecommendation:
            recommendation[user_id] = recommend(UserModels[user_id], isRec_start, isRec_end, 1, PopularItems)

    Data = []
    for user_id in recommendation:
        for item_id in recommendation[user_id]:
            Data.append((user_id, item_id))
    WriteCSV('predict22.csv', ['user_id', 'item_id'], Data)


    # hitNum, recall, precision = calRec(recommendation, UserModels, 2)
    # print 'HitNum: %d, Recall: %d, Precison: %d.' % (hitNum, recall, precision)
    # precision = float(hitNum)/precision
    # recall = float(hitNum)/recall
    # f1 = 2*recall*precision/(recall+precision)
    # print 'Precision: ', precision
    # print 'Recall: ', recall
    # print 'F1: ', f1



if __name__ == '__main__':
    mCConfig = CReadConfig("config.ini")
    parameters = mCConfig.getBasic()
    filename = parameters['filename']
    main(filename)