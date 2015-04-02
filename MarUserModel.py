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

    def add(self, item_id, category_id, behavior, timestamp):
        dayStamp = getDay(timestamp)
        if dayStamp not in self.dataDict:
            self.dataDict[dayStamp] = []
        self.dataDict[dayStamp].append((item_id, category_id, behavior))

    def preProcess(self):
        pass

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
                    if behavior == 4:
                        test.add(item_id)
            dayStamp += 86400

        self.train = train
        self.test = test


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
                if behavior == 4:
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

    def buildNGram(self, states, gram_n):
        statesFrozen = [frozenset([s]) for s in states]
        statesDict = {1: set(statesFrozen)}
        for i in range(gram_n-1):
            temp = set()
            for j in statesDict[i+1]:
                for k in statesDict[1]:
                    if len(j&k) != 0: continue
                    temp.add(j.union(k))
            statesDict[i+2] = temp
        return statesDict[gram_n]

    def recommend(self, predict_stamp, gram_n, statesDict, top_num):
        if len(self.train) == 0:
            return []
        max_stamp = max(self.train)
        if max_stamp != predict_stamp-86400:
            # print time.strftime('%Y-%m-%d', time.localtime(max_stamp)), time.strftime('%Y-%m-%d', time.localtime(predict_stamp))
            return []
        states = set()
        for item_id, category_id, behavior in self.train[max_stamp]:
            states.add(item_id)
        states = self.buildNGram(states, gram_n)
        recommendation = {}
        for s in states:
            if s in statesDict:
                for item_id in statesDict[s]:
                    if item_id not in recommendation:
                        recommendation[item_id] = 0
                    recommendation[item_id] += statesDict[s][item_id]
        recommendation = sorted(recommendation.iteritems(), key=lambda x:x[1], reverse=True)
        recommendation = [item_id for item_id, sim in recommendation[:top_num]]
        return recommendation

