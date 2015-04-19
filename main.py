#!usr/bin/env python
#coding:utf-8

import time
from preprocess.extractFeatures2 import extract
from ReadConf import CReadConfig


def main():
    mCConfig = CReadConfig("config.ini")
    parameters = mCConfig.getBasic()
    train_filename = parameters['filename']
    features_filename = 'features.csv'
    lastStamp = time.mktime(time.strptime('2014-12-17 0', '%Y-%m-%d %H'))
    pre_interval = 86400*20
    after_interval = 86400*1
    print 'Extracting features.'
    extract(train_filename, features_filename, lastStamp, pre_interval, after_interval)


if __name__ == '__main__':
    main()