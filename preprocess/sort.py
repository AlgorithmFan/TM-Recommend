#!usr/bin/env python
#coding:utf-8
import csv
import time

def sort(read_filename, write_filename):
    '''
    Extract features from the dataset.
    '''
    formatter = '%Y-%m-%d %H'

    read_fp = file(read_filename, 'rb')
    reader = csv.reader(read_fp)

    data = {}
    for line in reader:
        if reader.line_num == 1:
            continue
        user_id = int(line[0])
        item_id = int(line[1])
        behavior = int(line[2])
        geo = line[3]
        item_category = int(line[4])
        timestamp = int(time.mktime(time.strptime(line[5], formatter)))
        data.setdefault(user_id, dict())
        data[user_id].setdefault(item_id, list())
        data[user_id][item_id].append((behavior, geo, item_category, timestamp))
    read_fp.close()

    write_fp = file(write_filename, 'wb')
    writer = csv.writer(write_fp)
    for user_id in data:
        for item_id in data[user_id]:
            temp = data[user_id][item_id]
            temp.sort(key=lambda x:x[3])
            for behavior, geo, item_category, timestamp in temp:
                writer.writerow([user_id, item_id, behavior, geo, item_category, timestamp])
    write_fp.close()

if __name__ == '__main__':
    from ReadConf import CReadConfig
    mCConfig = CReadConfig("../config.ini")
    parameters = mCConfig.getBasic()
    read_filename = parameters['filename']
    write_filename = 'J:/DataSet/Competition/train_user_sort.csv'
    sort(read_filename, write_filename)






