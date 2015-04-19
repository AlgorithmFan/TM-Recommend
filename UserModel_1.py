#!usr/bin/env python
#coding:utf-8

import types
import time
import datetime
import numpy as np

Weight = {1:0.05, 2:0.15, 3:0.2, 4:0.6}

class CUserModel:
    def __init__(self, user_id):
        self.user_id = user_id
        self.Items = []
        self.flag = 'd'
        self.level = 0
        self.dataDict = None
        self.isRecommendation = False
        self.train = None
        self.test = None

    def addItem(self, item_id, behavior, user_geohash, timestamp):
        self.Items.append((item_id, behavior, user_geohash, timestamp))

    def sortItemsByTime(self):
        '''Sort the items order by time asc'''
        self.Items.sort(key=lambda x:x[3])

    def isRecommend(self, startstamp, endstamp):
        buy_num = 0
        flag = False
        level = 0
        for item_id, behavior, user_geohash, timestamp in self.Items:
            if behavior == 4:
                buy_num += 1
            if timestamp>=startstamp and timestamp < endstamp:
                flag = True
                if timestamp > level:
                    level = timestamp
        if buy_num and flag:
            self.isRecommendation = True
            self.level = 3600.0/(endstamp-level)
        else:
            self.isRecommendation = False

    def getBuyItems(self, endstamp):
        items = set()
        for item_id, behavior, user_geohash, timestamp in self.Items:
            if timestamp<endstamp and behavior==4:
                items.add(item_id)
        return items

    def splitDataByDay(self, startstamp, endstamp):
        '''
        Spliting the data according to day.
        '''
        train, test = [], set()
        for item_id, behavior, user_geohash, timestamp in self.Items:
            if timestamp >= startstamp and timestamp < endstamp:
                train.append((item_id, behavior, user_geohash, timestamp))
            elif timestamp>= endstamp and timestamp < endstamp+43200:
                if behavior == 4:
                    test.add(item_id)
        self.train = train
        self.test = test
