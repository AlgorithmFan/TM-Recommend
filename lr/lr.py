#!usr/bin/env python
#coding:utf-8

import random
import numpy as np
import csv
from sklearn.linear_model import LogisticRegression
from sklearn import cross_validation, preprocessing
from operator import itemgetter
import cPickle


def ReadFeatures(filename, columns=[3,4,5]):
    fp = file(filename, 'rb')
    reader = csv.reader(fp)
    features = []
    for line in reader:
        temp = []
        for column in columns:
            temp.append(float(line[column]))
        features.append([temp])
    fp.close()
    return np.array(features)

def get_model(filename, columns, lastStamp):
    positive_features = ReadFeatures('positive_'+filename, columns)
    negative_features = ReadFeatures('negative_'+filename, columns)
    print 'before sampling:'
    print positive_features.shape, negative_features.shape

    random.seed(0)
    index = random.randint(0, negative_features.shape[0]-positive_features.shape[0])
    negative_features = negative_features[index:index+positive_features.shape[0], :]
    print 'after sampling:'
    print positive_features.shape, negative_features.shape

    positive_label = np.ones(positive_features.shape[0])
    negative_label = np.zeros(negative_features.shape[0])

    X = np.append(positive_features, negative_features, axis=0)
    Y = np.append(positive_label, negative_label)

    for i, C in enumerate(10.0 ** np.arange(2, 3)):
        lr = LogisticRegression(C=C, penalty='12', tol=0.001)
        # print coss_validation.cross_val_score(lr, X, Y)
        model = lr.fit(X, Y)
        cPickle.dump(model, open('model.txt', 'w'))
        coef = model.coef_.ravel()
        print columns
        print coef

    return model

def get_recommend(model, columns, p_threshold, top_threshold, lastStamp):
    print '-----------------------'

