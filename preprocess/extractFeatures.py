#!usr/bin/env python
#coding:utf-8

'''
Extracting features from train_data.
'''

import csv
from operator import itemgetter
import time
import numpy

def time_weighted(t, t0):
    if t >= t0:
        print 'time weighted error: ', t, t0
    ret = numpy.exp(-float(t0 - t) / 5 / 86400)
    return ret

def extract(filename, endstamp):
    '''
    Extract features from the dataset.
    '''
    userItemBehaviorAll = dict()    # 用户的行为记录
    userPurchaseCount = dict()      # 用户购买item的个数
    itemPurchaseCount = dict()      # item的购买数
    userItemPurchaseCount = dict()  # 用户购买item的个数
    userItems = dict()              # 用户购买item
    itemUsers = dict()              # item购买的用户

    fp = file(filename, 'rb')
    reader = csv.reader(fp)

    for line in reader:
        if reader.line_num==1:
            continue
        user_id = int(line[0])
        item_id = int(line[1])
        behavior = int(line[2])
        geo = line[3]
        item_category = int(line[4])
        timestamp = int(line[5])

        if timestamp>=endstamp:
            continue

        userItemBehaviorAll.setdefault(user_id, dict())
        userItemBehaviorAll[user_id].setdefault(item_id, list())
        userItemBehaviorAll[user_id][item_id].append((behavior, item_category, timestamp))

        if behavior == 4:
            userItems.setdefault(user_id, set())
            userItems[user_id].add(item_id)

            itemUsers.setdefault(item_id, set())
            itemUsers[item_id].add(user_id)

            userPurchaseCount.setdefault(user_id, 0)
            userPurchaseCount[user_id] += 1

            itemPurchaseCount.setdefault(item_id, 0)
            itemPurchaseCount[item_id] += 1

            userItemPurchaseCount.setdefault((user_id, item_id), 0)
            userItemPurchaseCount[(user_id, item_id)] += 1

    #make sure that acts of (user, item) are ordered by date, act
    for user_id in userItemBehaviorAll.keys():
        for item_id, act_list in userItemBehaviorAll[user_id].items():
            userItemBehaviorAll[user_id][item_id] = sorted(act_list, key=itemgetter(2, 0))

    #Summarize user's avg clk and std before purchase{user_id: (mean, std), ...}
    #Only the first purchase is taken into consideration
    user_avg_before_purchase = dict()
    item_clk_count_before_purchase = dict()
    for user_id in userItemBehaviorAll.keys():
        clk_count = list()
        for item_id in userItemBehaviorAll[user_id].keys():
            for i in range(len(userItemBehaviorAll[user_id][item_id])):
                if userItemBehaviorAll[user_id][item_id][i][0] == 4:
                    purchase_day = userItemBehaviorAll[user_id][item_id][i][2]

                    count = 0
                    for j in range(i):
                        if userItemBehaviorAll[user_id][item_id][j][2] == purchase_day:
                            break

                        if userItemBehaviorAll[user_id][item_id][j][0] == 1:
                            count += time_weighted(userItemBehaviorAll[user_id][item_id][j][2], purchase_day)

                    if count != 0:
                        clk_count.append(count)
                    item_clk_count_before_purchase.setdefault(item_id, list())
                    item_clk_count_before_purchase[item_id].append(count)
                    break

        if len(clk_count) != 0:
            user_avg_before_purchase[user_id] = (numpy.mean(clk_count), numpy.std(clk_count))
        else:
            user_avg_before_purchase[user_id] = (0, 0)

    init_purchase_count = 0
    for user_id in userItemBehaviorAll.keys():
        if user_id in userPurchaseCount:
            u_purchase_count = userPurchaseCount[user_id]
        else:
            u_purchase_count = 0

        if user_id in userItems:
            u_item_count = len(userItems[user_id])
        else:
            u_item_count = 0

        for item_id in userItemBehaviorAll[user_id].keys():
            if item_id not in itemPurchaseCount:
                continue

            pre_purchase_index = -1
            pre_purchase_day = -1
            pre_purchase_count = init_purchase_count

            clk_before_purchase = 0
            cart_before_purchase = 0
            fav_before_purchase = 0

            if user_id in userItems and item_id in userItems[user_id]:
                pass

