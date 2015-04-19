#!usr/bin/env python
#coding:utf-8
import time
import csv
from ReadConf import CReadConfig
from CommonFunc import ReadUserModels, WriteCSV

def ReadWriteByDay(Filename):
    CsvFile = file(Filename, 'rb')
    reader = csv.reader(CsvFile)
    filenames = {}
    for line in reader:
        if reader.line_num==1:
            continue
        user_id = int(line[0])
        item_id = int(line[1])
        behavior = int(line[2])
        geo = line[3]
        item_category = int(line[4])
        if line[5][:10] not in filenames:
            filenames[line[5][:10]] = file('recommendation/'+line[5][:10]+'.csv', 'wb')
            filenames[line[5][:10]] = csv.writer(filenames[line[5][:10]])
        filenames[line[5][:10]].writerow([user_id, item_id, behavior,geo,  item_category, line[5]])



if __name__ == '__main__':
    mCConfig = CReadConfig("config.ini")
    parameters = mCConfig.getBasic()
    filename = parameters['filename']
    ReadWriteByDay(filename)