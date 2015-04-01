#!usr/bin/env python
#coding:utf-8

import types
import time
import datetime
import numpy as np
from GetTime import getMonth, getWeek, getDay

Weight = {1:0.05, 2:0.15, 3:0.2, 4:0.6}

class CUserModel:
    def __init__(self, user_id):
        self.user_id = user_id
        self.Items = []
        self.flag = 'd'
        self.dataDict = None
        self.train = None
        self.test = None

    def addItem(self, item_id, behavior, user_geohash, timestamp):
        self.Items.append((item_id, behavior, user_geohash, timestamp))

    def sortItemsByTime(self):
        '''Sort the items order by time asc'''
        self.Items.sort(key=lambda x:x[3])

    def staticData(self, ItemList, flag):
        '''
        Divide the data according to interval.
        '''
        self.flag = flag
        ItemLen = len(ItemList)
        ItemDict = {ItemList[i]: i for i in range(ItemLen)}
        self.sortItemsByTime()
        dataDict = {}
        for item_id, behavior, user_geohash, timestamp in self.Items:
            index = getDay(timestamp)
            if index not in dataDict:
                dataDict[index] = np.zeros(ItemLen, 'int')
            dataDict[index][ItemDict[item_id]] += Weight[behavior]
        self.DataDict = dataDict


    def splitDate(self, **parameters):
        '''
        Split the data into train dataset and test dataset according to interval.
        '''
        dateFuncDict = {'m': self.splitDataByMonth, 'w':self.splitDataByWeek, 'd':self.splitDataByDay}
        dateFunc = dateFuncDict[self.flag]
        train, test = dateFunc(**parameters)

        if len(train)==0:
            return False
        else:
            self.train = np.array(train)
            if len(test) == 0:
                self.test = np.zeros((1, self.train.shape[1]))
            else:
                self.test = np.array(test)
            index = np.nonzero(self.train.sum(axis=0)>0)
            self.test[:, index] = np.zeros(self.test[:, index].shape)
            return True

    def splitDataByDay(self, _year, _month, _day, _dateNum=30):
        '''
        Spliting the data according to day.
        '''
        dayStamp = int(time.mktime(time.strptime('%d-%d-%d' % (_year, _month, _day),'%Y-%m-%d')))
        train, test = [], []
        dateNum = _dateNum
        for i in range(dateNum):
            if dayStamp in self.dataDict:
                train.append(self.dataDict[dayStamp])
            dayStamp += 86400

        for i in range(1):
            if dayStamp in self.dataDict:
                test.append(self.dataDict[dayStamp])
            dayStamp += 86400

        return train, test

    def splitDataByMonth(self, _year, _month, _day, _dateNum = 12):
        '''
        Spliting the data according to month.
        '''
        train, test = [], []
        year, month, dateNum = _year, _month, _dateNum
        for i in range(dateNum):
            index = datetime.datetime(year=year, month=month, day=1)
            index = int(time.mktime(index.timetuple()))
            if index in self.dataDict:
                train.append(self.dataDict[index])
            month += 1
            if month>12:
                year += 1
                month = 1

        for i in range(1):
            index = datetime.datetime(year=year, month=month, day=1)
            index = int(time.mktime(index.timetuple()))
            if index in self.dataDict:
                test.append(self.dataDict[index])
            month += 1
            if month > 12:
                year += 1
                month -= 12

        return train, test

    def splitDataByWeek(self, _year, _month, _day,  _dateNum = 10):
        '''
        Spliting the data according to week.
        '''
        dayStamp = int(time.mktime(time.strptime('%d-%d-%d' % (_year, _month, _day),'%Y-%m-%d')))
        weekStamp = getWeek(dayStamp)
        train, test = [], []
        dateNum = _dateNum
        for i in range(dateNum):
            if weekStamp in self.dataDict:
                train.append(self.dataDict[weekStamp])
            weekStamp += 604800

        for i in range(1):
            if weekStamp in self.dataDict:
                test.append(self.dataDict[weekStamp])
            weekStamp += 604800

        return train, test

