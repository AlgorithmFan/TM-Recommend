#!usr/bin/env python
#coding:utf-8
import csv
import math

def ReadCSV(Filename):
    '''读取数据'''
    CsvFile = file(Filename, 'rb')
    reader = csv.reader(CsvFile)
    UserItemStamp = {}
    for line in reader:
        if reader.line_num==1:
            continue
        user_id = int(line[0])
        item_id = int(line[1])
        timestamp = int(float(line[2]))
        if user_id not in UserItemStamp:
            UserItemStamp[user_id] = []
        UserItemStamp[user_id].append((item_id, timestamp))
    return UserItemStamp

def calSubRecommendation1(UserItem, active_user_id, k_n):
    similarity = {}
    for user_id in UserItem:
        if user_id == active_user_id:
            continue
        comm = UserItem[user_id] & UserItem[active_user_id]
        if len(comm) == 0:
            continue
        supp = UserItem[user_id] | UserItem[active_user_id]
        similarity[user_id] = float(len(comm))/len(supp)
    similarity = sorted(similarity.iteritems(), key=lambda x:x[1], reverse=True)
    similarity = {user_id: sim for user_id, sim in similarity[:k_n]}
    recommendation = {}
    for user_id in similarity:
        for item_id in UserItem[user_id]:
            if item_id in UserItem[active_user_id]:
                continue
            if item_id not in recommendation:
                recommendation[item_id] = 0
            recommendation[item_id] += similarity[user_id]
    return recommendation

def calSubRecommendation2(UserItem, active_user_id, k_n):
    similarity = {}
    for user_id in UserItem:
        if user_id == active_user_id:
            continue
        sim = 0
        for item_id in UserItem[user_id]:
            if item_id not in UserItem[active_user_id]:
                continue
            interval = abs(UserItem[active_user_id][item_id]-UserItem[user_id][item_id])
            sim += math.exp(-float(interval)/86400)
        if sim>0:
            similarity[user_id] = sim

    similarity = sorted(similarity.iteritems(), key=lambda x:x[1], reverse=True)
    similarity = {user_id: sim for user_id, sim in similarity[:k_n]}
    recommendation = {}
    for user_id in similarity:
        for item_id in UserItem[user_id]:
            if item_id in UserItem[active_user_id]:
                continue
            if item_id not in recommendation:
                recommendation[item_id] = 0
            recommendation[item_id] += similarity[user_id]
    return recommendation


def recommend_2(UserItemStamp):
    UserItem = {}
    for user_id in UserItemStamp:
        UserItem[user_id] = {}
        for item_id, stamp in UserItemStamp[user_id]:
            if item_id not in UserItem[user_id]:
                UserItem[user_id][item_id] = stamp
            elif stamp > UserItem[user_id][item_id]:
                UserItem[user_id][item_id] = stamp
    recommendation = {}
    for user_id in UserItem:
        temp = calSubRecommendation2(UserItem, user_id, 50)
        temp = sorted(temp.iteritems(), key=lambda x:x[1], reverse=True)
        recommendation[user_id] = set([item_id for item_id, sim in temp[:10]])
    return recommendation

def recommend_1(UserItemStamp):
    UserItem = {}
    for user_id in UserItemStamp:
        UserItem[user_id] = set()
        for item_id, stamp in UserItemStamp[user_id]:
            UserItem[user_id].add(item_id)

    recommendation = {}
    for user_id in UserItem:
        temp = calSubRecommendation1(UserItem, user_id, 50)
        temp = sorted(temp.iteritems(), key=lambda x:x[1], reverse=True)
        recommendation[user_id] = set([item_id for item_id, sim in temp[:10]])
    return recommendation

def splitData(UserItemStamp, endstamp):
    train = {}
    test = {}
    for user_id in UserItemStamp:
        train[user_id] = []
        test[user_id] = set()
        for item_id, stamp in UserItemStamp[user_id]:
            if stamp <=endstamp:
                train[user_id].append((item_id, stamp))
            elif stamp <= endstamp+86400:
                test[user_id].add(item_id)
    return train, test


if __name__ == '__main__':
    import time
    print 'Step 1: Load data.'
    filename = r'J:\DataSet\Competition\train_buy.csv'
    mUserItemStamp = ReadCSV(filename)

    print 'Step 2: Recommend'
    hit, pre, recall = 0, 0, 0
    for i in range(3):
        endstamp = time.mktime(time.strptime('2014-12-16', '%Y-%m-%d'))+i*86400
        train, test = splitData(mUserItemStamp, endstamp)
        recommendation = recommend_2(train)

        for user_id in recommendation:
            pre += len(recommendation[user_id])
            recall += len(test[user_id])
            hit += len(recommendation[user_id]&test[user_id])

        print 'Hit: %d, Precision: %d, Recall: %d.' % (hit, pre, recall)
        precision =  float(hit)/pre
        recall =  float(hit)/recall
        f1 = 2*precision*recall/(precision+recall)
        print 'Precison: ', precision
        print 'Recall: ', recall
        print 'F1: ', f1