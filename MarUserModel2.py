#!usr/bin/env python
#coding:utf-8
from GetTime import getDay
import time

class CUserModel:
    def __init__(self, user_id):
        self.user_id = user_id
        self.dataDict = {}
        self.train = None
        self.test = None
        self.categoryStates = {}
        self.itemsStates = {}


    def add(self, item_id, category_id, behavior, timestamp):
        dayStamp = getDay(timestamp)
        if dayStamp not in self.dataDict:
            self.dataDict[dayStamp] = []
        self.dataDict[dayStamp].append((item_id, category_id, behavior))

    def splitDataByDay(self, _year, _month, _day, _dateNum=30):
        '''
        Spliting the data according to day.
        '''
        dayStamp = int(time.mktime(time.strptime('%d-%d-%d' % (_year, _month, _day),'%Y-%m-%d')))
        train, test = {}, set()
        dateNum = _dateNum
        for i in range(dateNum):
            if dayStamp in self.dataDict:
                train[dayStamp] = self.dataDict[dayStamp]
            dayStamp += 86400

        for i in range(1):
            if dayStamp in self.dataDict:
                for item_id, category_id, behavior in self.dataDict[dayStamp]:
                    test.add(item_id)
            dayStamp += 86400

        self.train = train
        self.test = test

    def buildCategoryStates(self, gram_n=2):
        temp = sorted(self.train.iteritems(), key=lambda x:x[0])
        day_num = len(temp)
        states = {}
        for index in range(day_num-1):
            next_daystamp = temp[index+1][0]
            pre_daystamp = temp[index][0]
            if next_daystamp - pre_daystamp > 86400:
                continue

            for item_id, category_id, behavior in temp[index]



    def buildStates(self, gram_n=2):
        temp = sorted(self.train.iteritems(), key=lambda x:x[0])
        day_num = len(temp)
        states = {}
        for index in range(day_num-1):
            next_daystamp = temp[index+1][0]
            pre_daystamp = temp[index][0]
            if next_daystamp-pre_daystamp>86400:
                continue
            buyset = set()
            for item_id, category_id, behavior in temp[index+1][1]:
                if behavior != 1:
                    buyset.add(item_id)

            if len(buyset) == 0:
                continue
            pre_items = set()
            for item_id, category_id, behavior in temp[index][1]:
                pre_items.add(item_id)

            pre_states = self.buildNGram(pre_items, gram_n)
            for s in pre_states:
                states[s] = buyset
        return states