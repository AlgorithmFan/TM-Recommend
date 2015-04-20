#!usr/bin/env python
#coding:utf-8

import numpy as np
from CommonFunc import ReadData
from operator import itemgetter
import csv

gamma = 86400*5
PURCHASE = 4
CART = 3
FAVORATE = 2
CLICK = 1

POSITIVE = 1
TEST_POSITIVE = 2
NEGATIVE = 0
TEST_NEGATIVE = 3

def timeweight(behavior, pre_timestamp, cur_timestamp):
    if behavior == CLICK:
        return np.exp(float(pre_timestamp-cur_timestamp)/gamma)
    elif behavior == FAVORATE:
        return 1
    elif behavior == CART:
        return 1
    elif behavior == PURCHASE:
        return 1
    else:
        return 0


def extract(dataFilename, featuresFilename, lastStamp, pre_interval, after_interval):
    print 'Read Data from %s.' % dataFilename
    behaviorData, ItemCategory = ReadData(dataFilename, lastStamp)       # {user_id: {item_id: [(geo,behavior, timestamp), ...], ...}, ....}
    print 'The number of users is %d.' % len(behaviorData)
    print 'The number of items is %d.' % len(ItemCategory)

    print 'Sort the data by time and behavior type.'
    for user_id in behaviorData:
        for item_id in behaviorData[user_id]:
            behaviorData[user_id][item_id].sort(key=itemgetter(2, 0))

    #统计用户在购买item之前的点击次数
    print 'Static user_item.'
    user_item_count_before_purchase = dict()    #记录用户在购买item之前的点击行为
    user_purchase_num = dict()
    user_purchase_unique_num = dict()
    item_purchase_num = dict()
    item_purchase_unique_num = dict()
    user_lastStamp = dict()
    for user_id in behaviorData:
        user_item_count_before_purchase.setdefault(user_id, dict())
        user_lastStamp.setdefault(user_id, 0)
        #用户购买item的唯一数量
        user_purchase_unique_num.setdefault(user_id, 0)
        user_purchase_unique_num[user_id] += len(behaviorData[user_id])

        #用户购买item的数量
        user_purchase_num.setdefault(user_id, 0)
        for item_id in behaviorData[user_id]:
            user_item_count_before_purchase[user_id].setdefault(item_id, [])
            item_purchase_num.setdefault(item_id, 0)        #item被购买的数量
            item_purchase_unique_num.setdefault(item_id, set()) #item唯一被购买的用户数
            behavior_num = len(behaviorData[user_id][item_id])
            flag = False
            for i in range(behavior_num-1, -1, -1):
                behavior, geo, timestamp = behaviorData[user_id][item_id][i]
                if behavior == PURCHASE and flag is False:
                    cur_timestamp = timestamp
                    user_purchase_num[user_id] += 1             #用户购买item的数量
                    item_purchase_num[item_id] += 1             #item被购买的数量
                    item_purchase_unique_num[item_id].add(user_id)
                    user_item_count_before_purchase[user_id][item_id].append(0)
                    if user_lastStamp[user_id] < cur_timestamp: #获得用户购买item的最后一次时间，用于构建负样例
                        user_lastStamp[user_id] = cur_timestamp
                    flag = True
                elif behavior == PURCHASE and flag is True:
                    user_purchase_num[user_id] += 1             #用户购买item的数量
                    item_purchase_num[item_id] += 1             #item被购买的数量
                    item_purchase_unique_num[item_id].add(user_id)
                    user_item_count_before_purchase[user_id][item_id].append(0)
                    cur_timestamp = timestamp
                elif flag is True:
                    user_item_count_before_purchase[user_id][item_id][-1] += timeweight(behavior, timestamp, cur_timestamp)
            if len(user_item_count_before_purchase[user_id][item_id]) == 0:
                del user_item_count_before_purchase[user_id][item_id]
        #如果用户没有购买行为，则将其删除
        if len(user_item_count_before_purchase[user_id]) == 0:
            del user_item_count_before_purchase[user_id]

