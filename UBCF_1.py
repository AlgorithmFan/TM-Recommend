#!usr/bin/env python
#coding:utf-8

from UserBasedCF_1 import CUserBasedCF
from FileTxt import CRecords
from CommFunc import calRec
from ReadConf import CReadConfig
import time

def main(UserModels, ItemList, parameters):
    hitNum10, recNum10, preNum10 = 0, 0, 0
    hitNum5, recNum5, preNum5 = 0, 0, 0

    mCRecords10 = CRecords(r'recommendation/UBCF_1%s_t%d_a%d.txt' % (parameters['date_flag'], 10, parameters['items_thr']))
    mCRecords5 = CRecords(r'recommendation/UBCF_1%s_t%d_a%d.txt' % (parameters['date_flag'], 5, parameters['items_thr']))
    mCRecords10.writeDescription(parameters['description'])
    mCRecords5.writeDescription(parameters['description'])
    mCRecords10.writeParameters(parameters)
    mCRecords5.writeParameters(parameters)

    copy_UsersModels = UserModels.copy()
    UserBasedCF = CUserBasedCF()

    dayStamp = time.mktime(time.strptime('2014-11-18', '%Y-%m-%d'))
    thr = time.mktime(time.strptime('2014-12-18', '%Y-%m-%d'))
    date_num = parameters['date_num']
    while dayStamp < thr:
        dayStr = time.localtime(dayStamp)
        year, month, day = dayStr.tm_year, dayStr.tm_mon, dayStr.tm_mday
        print '*'*100
        print 'Date from %s-%s-%s, dateNum: %d.' % (year, month, day, date_num)
        UserModels = copy_UsersModels.copy()

        for user_id in UserModels.keys():
            flag = UserModels[user_id].splitDate(_year=year, _month=month, _day=day, _dateNum = date_num)
            if flag == False:  del UserModels[user_id]

        print 'The number of users is %d.' % len(UserModels)
        print 'The number of items is %d.' % len(ItemList)

        if len(UserModels) != 0:
            recommendation = UserBasedCF.calRecommend(UserModels, ItemList, parameters['top_num'])
        else:
            recommendation = {}

        h, r, p = calRec(recommendation, UserModels, 10)
        recNum10 += r
        preNum10 += p
        hitNum10 += h
        print 'Hit: %d, Recall: %d, Precision: %d, UsersNum: %d.' % (h, r, p, len(mUserModels.keys()))
        mCRecords10.writeHRP(date_num, h, r, p)


        h, r, p = calRec(recommendation, UserModels, 5)
        recNum5 += r
        preNum5 += p
        hitNum5 += h
        mCRecords5.writeHRP(date_num, h, r, p)

        if parameters['date_flag'] == 'm':
            month += parameters['date_interval']
            if month > 12:
                year += 1
                month -= 12
            dayStamp = time.mktime(time.strptime('%d-%d-%d' % (year, month, day),'%Y-%m-%d'))
        elif parameters['date_flag'] == 'w':
            dayStamp += 604800*parameters['date_interval']
        elif parameters['date_flag'] == 'd':
            dayStamp += 86400*parameters['date_interval']

    print '*'*100
    print 'artists_thr: %d.' % parameters['items_thr']
    recall = float(hitNum10)/recNum10
    precision = float(hitNum10)/preNum10
    f1 = 2*recall*precision/(recall+precision)
    print 'HitNum: ', hitNum10
    print 'Recall: %d, %f.' % (recNum10, recall)
    print 'Precision: %d, %f.' % (preNum10, precision)
    print 'F1: ', f1
    mCRecords10.writeDescription('artists_thr: %d.\n' % parameters['items_thr'])
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
    mCRecords5.writeDescription('artists_thr: %d.\n' % parameters['items_thr'])
    mCRecords5.writeDescription('Recall: %d, %f.\n' % (recNum5, recall))
    mCRecords5.writeDescription('Precision: %d, %f.\n' % (preNum5, precision))
    mCRecords5.writeDescription('F1: %f\n' % f1)
    mCRecords5.close()

if __name__ == '__main__':
    from CommFunc import ReadUserModels
    mCConfig = CReadConfig("config.ini")
    parameters = mCConfig.getUBCF()

    for key in parameters:
        print key, parameters[key]

    filename = r'J:\DataSet\Competition\train_user.csv'
    print 'Load UserModels.'
    mUserModels, mItems = ReadUserModels(filename)

    print 'The number of items is %d.' % len(mItems)

    parameters['description'] += filename
    main(mUserModels, mItems, parameters)

