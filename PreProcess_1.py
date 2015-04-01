#!usr/bin/env python
#coding:utf-8

from CommFunc import ReadUserModels
import csv
import time

def SplitDataBasedOnBehavior(Filename, click_filename, favorate_filename, shop_filename, buy_filename):
    '''读取数据'''
    formatter = '%Y-%m-%d %H'
    CsvFile = file(Filename, 'rb')
    reader = csv.reader(CsvFile)
    click_fp = file(click_filename, 'wb')
    favt_fp = file(favorate_filename, 'wb')
    shop_fp = file(shop_filename, 'wb')
    buy_fp = file(buy_filename, 'wb')
    fp_choise = {1: csv.writer(click_fp), 2: csv.writer(favt_fp), 3: csv.writer(shop_fp), 4: csv.writer(buy_fp)}
    for line in reader:
        if reader.line_num==1:
            continue
        user_id = int(line[0])
        item_id = int(line[1])
        behavior = int(line[2])
        item_category = int(line[4])
        timestamp = int(time.mktime(time.strptime(line[5], formatter)))
        fp_choise[behavior].writerow([user_id, item_id, item_category, timestamp])
    CsvFile.close()
    click_fp.close()
    favt_fp.close()
    shop_fp.close()
    buy_fp.close()

def sort_data(read_filename, path):
    formatter = '%Y-%m-%d %H'
    read_file = file(read_filename, 'rb')
    read_csv =  csv.reader(read_file)
    UserItemCategGeoStamp = {}
    for line in read_csv:
        if read_csv.line_num==1:
            continue
        user_id = int(line[0])
        item_id = int(line[1])
        behavior = int(line[2])
        geo = line[3]
        item_category = int(line[4])
        timestamp = int(time.mktime(time.strptime(line[5], formatter)))
        if user_id not in UserItemCategGeoStamp:
            UserItemCategGeoStamp[user_id] = []
        UserItemCategGeoStamp[user_id].append((item_id, behavior, geo, item_category, timestamp))
    read_file.close()

    Users = UserItemCategGeoStamp.keys()
    num = len(Users)
    for i in range(10):
        write_file = file(path+'train_%d.csv' % i, 'wb')
        write_csv = csv.writer(write_file)
        start_index = i*num/10
        end_index = (i+1)*num/10
        for user_id in Users[start_index:end_index]:
            temp = UserItemCategGeoStamp[user_id]
            temp.sort(key=lambda x:x[4])
            data = [(user_id, item_id, item_category, behavior, geo, timestamp) for item_id, behavior, geo, item_category, timestamp in temp]
            write_csv.writerows(data)
        write_file.close()



if __name__ == '__main__':
    print 'Download User file.'
    filename = r'J:\DataSet\Competition\train_user.csv'
    # click_filename = r'J:\DataSet\Competition\train_click1.csv'
    # favt_filename = r'J:\DataSet\Competition\train_favt1.csv'
    # shop_filename = r'J:\DataSet\Competition\train_shop1.csv'
    # buy_filename = r'J:\DataSet\Competition\train_buy1.csv'
    # SplitDataBasedOnBehavior(filename, click_filename, favt_filename, shop_filename, buy_filename)

    path = r'J:/DataSet/Competition/'
    sort_data(filename, path)