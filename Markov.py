#!usr/bin/env python
#coding:utf8

'''
主要利用前N天的信息来预测，用户在第N+1天对哪些产品或者品牌感兴趣，因此可以对这两部分进行预测。
Markorv：
'''
import csv
import time
from MarUserModel import CUserModel
from FileTxt import CRecords
from ReadConf import CReadConfig

def calRec(recommendation, UserModels, top_num):
    hitNum, recall, precision = 0, 0, 0
    for user_id in recommendation:
        precision += len(recommendation[user_id][:top_num])
        recall += len(UserModels[user_id].test)
        hitNum += len(UserModels[user_id].test & set(recommendation[user_id][:top_num]))

    return hitNum, recall, precision

def ReadUserModels(Filename):
    '''读取数据'''
    formatter = '%Y-%m-%d %H'
    CsvFile = file(Filename, 'rb')
    reader = csv.reader(CsvFile)
    UserModels = {}
    ItemSet = set()
    for line in reader:
        if reader.line_num==1:
            continue
        if reader.line_num > 10000000:
            break
        user_id = int(line[0])
        item_id = int(line[1])
        behavior = int(float(line[2]))
        # if behavior == 1:
        #     continue
        geo = line[3]
        item_category = int(line[4])
        timestamp = int(time.mktime(time.strptime(line[5], formatter)))
        if user_id not in UserModels:
            UserModels[user_id] = CUserModel(user_id)
        UserModels[user_id].add(item_id, item_category, behavior, timestamp)
        ItemSet.add(item_id)

    # ItemList = list(ItemSet)
    print 'The number of items is %d.' % len(ItemSet)
    print 'The number of users is %d.' % len(UserModels)
    return UserModels


def buildMarkov(UserModels, gram_n):
    '''
    根据用户的行为记录，构建马尔科夫链
    '''
    print 'Building Association.'
    statesDict = {}
    for user_id in UserModels:
        states = UserModels[user_id].buildStates(gram_n)
        for s in states:
            if s not in statesDict:
                statesDict[s] = {}
            for item_id in states[s]:
                if item_id not in statesDict[s]:
                    statesDict[s][item_id] = 0
                statesDict[s][item_id] += 1

    # for s in statesDict:
    #     s1 = 0
    #     for item_id in statesDict[s]:
    #         s1 += states[s][item_id]
    #     for item_id in statesDict[s]:
    #         statesDict[s][item_id] = float(statesDict[s][item_id])/s1
    print 'The number of dicts is %d.' % len(statesDict)
    return statesDict


def main(Filename, Parameters):
    UserModels = ReadUserModels(Filename)
    gram_n = Parameters['gram_n']
    hitNum10, recNum10, preNum10 = 0, 0, 0
    hitNum5, recNum5, preNum5 = 0, 0, 0

    mCRecords10 = CRecords(r'recommendation/Markov_1%s_t%d.txt' % (Parameters['date_flag'], 10))
    mCRecords5 = CRecords(r'recommendation/Markov_1%s_t%d.txt' % (Parameters['date_flag'], 5))
    mCRecords10.writeDescription(Parameters['description'])
    mCRecords5.writeDescription(Parameters['description'])
    mCRecords10.writeParameters(Parameters)
    mCRecords5.writeParameters(Parameters)


    dayStamp = time.mktime(time.strptime('2014-11-18', '%Y-%m-%d'))
    thr = time.mktime(time.strptime('2014-12-18', '%Y-%m-%d'))
    date_num = Parameters['date_num']
    dayStr = time.localtime(dayStamp)

    year, month, day = dayStr.tm_year, dayStr.tm_mon, dayStr.tm_mday
    while date_num < 31:
        print '*'*100
        print 'Date from %s-%s-%s, dateNum: %d.' % (year, month, day, date_num)

        for user_id in UserModels.keys():
            UserModels[user_id].splitDataByDay(_year=year, _month=month, _day=day, _dateNum = date_num)
            # UserModels[user_id].buildStates(gram_n)

        if len(UserModels) != 0:
            statesDict = buildMarkov(UserModels, gram_n)
            recommendation = {}
            print 'Recommendation ........'
            for user_id in UserModels:
                recommendation[user_id] = UserModels[user_id].recommend(dayStamp+date_num*86400, gram_n, statesDict, 10)

        else:
            recommendation = {}

        h, r, p = calRec(recommendation, UserModels, 10)
        recNum10 += r
        preNum10 += p
        hitNum10 += h
        print 'Hit: %d, Recall: %d, Precision: %d, UsersNum: %d.' % (h, r, p, len(UserModels.keys()))
        mCRecords10.writeHRP(date_num, h, r, p)

        h, r, p = calRec(recommendation, UserModels, 5)
        recNum5 += r
        preNum5 += p
        hitNum5 += h
        mCRecords5.writeHRP(date_num, h, r, p)

        date_num += Parameters['date_interval']

    print '*'*100
    # print 'artists_thr: %d.' % Parameters['items_thr']
    recall = float(hitNum10)/recNum10
    precision = float(hitNum10)/preNum10
    f1 = 2*recall*precision/(recall+precision)
    print 'HitNum: ', hitNum10
    print 'Recall: %d, %f.' % (recNum10, recall)
    print 'Precision: %d, %f.' % (preNum10, precision)
    print 'F1: ', f1
    # mCRecords10.writeDescription('artists_thr: %d.\n' % Parameters['items_thr'])
    mCRecords10.writeDescription('Recall: %d, %f.\n' % (recNum10, recall))
    mCRecords10.writeDescription('Precision: %d, %f.\n' % (preNum10, precision))
    mCRecords10.writeDescription('F1: %f\n' % f1)
    mCRecords10.close()

    recall = float(hitNum5)/recNum5
    precision = float(hitNum5)/preNum5
    f1 = 2*recall*precision/(recall+precision)
    print 'HitNum: ', hitNum5
    print 'Recall: %d, %f.' % (recNum5, recall)
    print 'Precision: %d, %f.' % (preNum5, precision)
    print 'F1: ', f1
    # mCRecords5.writeDescription('artists_thr: %d.\n' % Parameters['items_thr'])
    mCRecords5.writeDescription('Recall: %d, %f.\n' % (recNum5, recall))
    mCRecords5.writeDescription('Precision: %d, %f.\n' % (preNum5, precision))
    mCRecords5.writeDescription('F1: %f\n' % f1)
    mCRecords5.close()


if __name__ == '__main__':
    # filename = r'/home/zhd/Dataset/Competition/train_user.csv'
    mCConfig = CReadConfig("config.ini")
    parameters = mCConfig.getMarkov()
    filename = parameters['filename']
    main(filename, parameters)


