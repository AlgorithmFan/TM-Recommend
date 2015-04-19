#!usr/bin/env python
#coding:utf-8
'''
# 用户所关注的Items
# 用户所关注的分类
# Item受欢迎程度
# 随时间的
'''
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
        return np.exp((pre_timestamp-cur_timestamp)/gamma)
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
    behaviorData, ItemCategory = ReadData(dataFilename)       # {user_id: {item_id: [(geo,behavior, timestamp), ...], ...}, ....}
    print 'The number of users is %d.' % len(behaviorData)
    print 'The number of items is %d.' % len(ItemCategory)

    print 'Sort the data by time and behavior type.'
    for user_id in behaviorData:
        for item_id in behaviorData[user_id]:
            behaviorData[user_id][item_id].sort(key=itemgetter(2,0))

    #统计用户在购买item之前的点击次数
    print 'Static user_item.'
    user_item_count_before_purchase = dict()    #记录用户在购买item之前的点击行为
    for user_id in behaviorData:
        user_item_count_before_purchase.setdefault(user_id, dict())
        for item_id in behaviorData[user_id]:
            user_item_count_before_purchase[user_id].setdefault(item_id, [0])
            behavior_num = len(behaviorData[user_id][item_id])
            for i in range(behavior_num):
                geo, behavior, timestamp = behaviorData[user_id][item_id][i]
                if timestamp >= lastStamp: #如果行为时间超过最终的时间，则此条记录删除，主要用于计算测试集
                    continue
                if behavior != PURCHASE:   #如果用户点击了item，则最后一个数字+1
                    user_item_count_before_purchase[user_id][item_id][-1] += 1
                    #最后一条记录，如果不是购买记录，则
                    # user_item_count_before_purchase[user_id][item_id]的最后一条记录没有用处，应删除
                    if i == behavior_num-1:
                        del user_item_count_before_purchase[user_id][item_id][-1]
                elif behavior == PURCHASE: #如果用户购买了item，则增加一条记录
                    if i != behavior_num-1:
                        user_item_count_before_purchase[user_id][item_id].append(0)

            if len(user_item_count_before_purchase[user_id][item_id]) < 1:  # 如果用户没有购买该item，则将该用户的item删除
                del user_item_count_before_purchase[user_id][item_id]
            elif user_item_count_before_purchase[user_id][item_id][-1] == 0:
                del user_item_count_before_purchase[user_id][item_id][-1]
                if len(user_item_count_before_purchase[user_id][item_id]) == 0:
                    del user_item_count_before_purchase[user_id][item_id]
        if len(user_item_count_before_purchase[user_id]) < 1:       # 如果用户没有购买过，则将用户删除
            del user_item_count_before_purchase[user_id]

    user_before_purchase = dict()
    item_before_purchase = dict()
    print 'User before purchase and item before purchase'
    for user_id in user_item_count_before_purchase:
        for item_id in user_item_count_before_purchase[user_id]:
            if len(user_item_count_before_purchase[user_id][item_id]) > 0:      #统计用户点击了item后购买的行为，长度小于等于1的，表示没有购买的item
                user_before_purchase.setdefault(user_id, list())
                item_before_purchase.setdefault(item_id, list())
                user_before_purchase[user_id].extend(user_item_count_before_purchase[user_id][item_id])
                item_before_purchase[item_id].extend(user_item_count_before_purchase[user_id][item_id])

    print 'Calculate the mean and variance of user_before_purchase.'
    user_avg_before_purchase = dict()
    for user_id in user_before_purchase.keys():
        # 用户在购买前的平均点击次数和方差
        user_avg_before_purchase[user_id] = (np.mean(user_before_purchase[user_id]), np.std(user_before_purchase[user_id]))
        # # 进行归一化处理
        # user_before_purchase[user_id] = (np.array(user_before_purchase[user_id]) - user_avg_before_purchase[user_id][0])/user_avg_before_purchase[user_id][1]

    print 'Calculate the mean and variance of item_before_purchase.'
    item_avg_before_purchase = dict()
    for item_id in item_before_purchase.keys():
        # Item在被购买前的平均点击次数和方差
        item_avg_before_purchase[item_id] = (np.mean(item_before_purchase[item_id]), np.std(item_before_purchase[item_id]))
        # # Item进行归一化处理
        # item_before_purchase[item_id] = (np.array(item_before_purchase[item_id]) - item_avg_before_purchase[item_id][0])/item_avg_before_purchase[item_id][1]

    print 'Static Positive Samples and Negative Samples.'
    positive_fp = file('in/positive_'+featuresFilename, 'wb')
    negative_fp = file('in/negative_'+featuresFilename, 'wb')
    positive_csv = csv.writer(positive_fp)
    negative_csv = csv.writer(negative_fp)
   # BehaviorCSV = {NEGATIVE: negative_csv, POSITIVE: positive_csv, TEST_POSITIVE: test_pos_csv, TEST_NEGATIVE: test_neg_csv}

    for user_id in behaviorData:
        if user_id in user_before_purchase:
            u_purchase_count = len(user_before_purchase[user_id])
        else:
            u_purchase_count = 0

        if user_id in user_item_count_before_purchase:
            u_unique_count = len(user_item_count_before_purchase[user_id])
        else:
            u_unique_count = 0

        for item_id in behaviorData[user_id]:
            if item_id not in item_before_purchase:
                continue

            behavior_before_purchase = {CLICK: 0, FAVORATE: 0, CART: 0, PURCHASE:0}
            # 如果用户购买了某item，则统计其正样例
            if user_id in user_item_count_before_purchase and item_id in user_item_count_before_purchase[user_id]:
                train_flag, test_flag = False, False
                for i in range(len(behaviorData[user_id][item_id])-1, -1):
                    geo, behavior, timestamp = behaviorData[user_id][item_id][i]
                    if timestamp>=lastStamp:
                        continue
                    if behavior == PURCHASE and train_flag is False:
                        cur_timestamp = timestamp
                        behavior_before_purchase[PURCHASE] = 1
                        train_flag = True
                    elif behavior == PURCHASE and train_flag is True:
                        positive_csv.writerow(user_id, item_id,
                                              len(user_item_count_before_purchase[user_id][item_id]) - 1 - behavior_before_purchase[PURCHASE],
                                              behavior_before_purchase[PURCHASE],
                                              behavior_before_purchase[CLICK],
                                              behavior_before_purchase[FAVORATE],
                                              behavior_before_purchase[CART],
                                              behavior_before_purchase[CLICK]-user_avg_before_purchase[user_id][0],
                                              user_avg_before_purchase[user_id][1],
                                              behavior_before_purchase[CLICK]-item_avg_before_purchase[item_id][0],
                                              item_avg_before_purchase[item_id][1],
                                              u_purchase_count,
                                              len(item_before_purchase[item_id]),
                                              u_unique_count,
                                              # len(item_before_purchase[item_])
                                              len(user_item_count_before_purchase[user_id][item_id]),
                                            )
                        behavior_before_purchase = {CLICK: 0, FAVORATE: 0, CART: 0, PURCHASE:behavior_before_purchase[PURCHASE]+1}
                        cur_timestamp = timestamp
                    elif train_flag is True:
                        behavior_before_purchase[behavior] += timeweight(behavior, timestamp, cur_timestamp)

            else:
                #only those who has no act in recent month are treated as negative case
                #For others, we predict whether purchase will happen after last day, so we assume the purchase day as
                #(last_day + 1)
                for i in range(len(behaviorData[user_id][item_id])-1, -1):
                    geo, behavior, timestamp = behaviorData[user_id][item_id][i]
                    if timestamp>=lastStamp:
                        continue
                    if timestamp>=lastStamp-pre_interval and timestamp<=lastStamp-after_interval:
                        behavior_before_purchase[behavior] += timeweight(behavior, timestamp, lastStamp)

                negative_csv.writerow(user_id, item_id,
                                      len(user_item_count_before_purchase[user_id][item_id]) - 1 - behavior_before_purchase[PURCHASE],
                                      behavior_before_purchase[PURCHASE],
                                      behavior_before_purchase[CLICK],
                                      behavior_before_purchase[FAVORATE],
                                      behavior_before_purchase[CART],
                                      behavior_before_purchase[CLICK]-user_avg_before_purchase[user_id][0],
                                      user_avg_before_purchase[user_id][1],
                                      behavior_before_purchase[CLICK]-item_avg_before_purchase[item_id][0],
                                      item_avg_before_purchase[item_id][1],
                                      u_purchase_count,
                                      len(item_before_purchase[item_id]),
                                      u_unique_count,
                                      # len(item_before_purchase[item_])
                                      len(user_item_count_before_purchase[user_id][item_id]),
                                    )

    positive_fp.close()
    negative_fp.close()


if __name__ == '__main__':
    import time
    from ReadConf import CReadConfig
    mCConfig = CReadConfig("config.ini")
    parameters = mCConfig.getBasic()
    train_filename = parameters['filename']
    features_filename = 'features.txt'
    lastStamp = time.mktime(time.strptime('2014-12-17 0', '%Y-%m-%d %H'))
    pre_interval = 86400*20
    after_interval = 86400*1
    extract(train_filename, features_filename, lastStamp, pre_interval, after_interval)




















