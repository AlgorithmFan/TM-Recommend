#!usr/bin/env python
#coding:utf8

from CommFunc import ReadUserItems, WriteCSV
from matplotlib.dates import MonthLocator, DayLocator, DateFormatter
import datetime
import matplotlib.pyplot as plt
import csv
from GetTime import getMonth, getWeek, getDay

def transfer(UserItems, ItemCategoryDict):
    ItemCatSort = sorted(ItemCategoryDict.iteritems(), key=lambda x:x[1])
    ItemList = [item_id for item_id, cat_id in ItemCatSort]
    ItemDict = {ItemList[i]:i for i in range(len(ItemList))}
    rUserItems = {}
    for user_id in UserItems:
        rUserItems[user_id] = set()
        for item_id, stamp in UserItems[user_id]:
            rUserItems[user_id].add(ItemDict[item_id])
    return rUserItems, ItemList

def ReadBuyCSV(Filename):
    '''读取数据'''
    CsvFile = file(Filename, 'rb')
    reader = csv.reader(CsvFile)
    UserItems = {}
    for line in reader:
        if reader.line_num==1:
            continue
        user_id = int(line[0])
        item_id = int(line[1])
        timestamp = int(line[2])
        if user_id not in UserItems:
            UserItems[user_id] = set()
        UserItems[user_id].add(item_id)
    return UserItems

def ShowUserItem(UserItems):
    '''显示用户使用了哪些Item'''
    fig, ax = plt.subplots()
    plt.title('User ID & Item ID ')
    plt.xlabel('Item ID')
    plt.ylabel('User ID')
    for user_id in UserItems:
        x = list(UserItems[user_id])
        y = [user_id] * len(x)
        plt.plot(x, y, '.')
    ax.grid(True)

def ShowUserTime(UserStamp):
    '''显示所有用户在时间上的连续性'''
    days = DayLocator()
    monthFmt = DateFormatter('%m-%d')

    fig, ax = plt.subplots()
    plt.title('Time(%s) & User ID ' % 'd')
    plt.xlabel('Time')
    plt.ylabel('User ID')
    for user_id in UserStamp:
        Users, dates = [], []
        for stamp in UserStamp[user_id]:
            Users.append(user_id)
            dates.append(stamp)
        ax.plot_date(dates, Users, '.')

    # format the ticks
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(monthFmt)
    ax.xaxis.set_minor_locator(days)
    ax.autoscale_view()

    # format the coords message box
    def price(x): return '$%1.2f'%x
    ax.fmt_xdata = DateFormatter('%Y-%m-%d')
    ax.fmt_ydata = price
    ax.grid(True)

    fig.autofmt_xdate()


def main():
    print 'Download User file.'
    filename = r'J:\DataSet\Competition\train_user.csv'
    mUserItems, mItemDict = ReadUserItems(filename, 1)
    print 'The number of users is %d.' % len(mUserItems)
    print 'The number of items is %d.' % len(mItemDict)

    print 'Write User Item.'
    Data = []
    for user_id in mUserItems:
        for item_id, stamp in mUserItems[user_id]:
            Data.append((user_id, item_id, stamp))
    filename = r'J:\DataSet\Competition\train_click.csv'
    mColumnHeader = ['user_id', 'item_id', 'timestamp']
    WriteCSV(filename, mColumnHeader, Data)

    print 'Write Item Category.'
    filename = r'J:\DataSet\Competition\train_click_category.csv'
    mColumnHeader = ['item_id', 'category_id']
    Data = []
    for item_id in mItemDict:
        for cag_id in mItemDict[item_id]:
            Data.append((item_id, cag_id))
    WriteCSV(filename, mColumnHeader, Data)

    mUserItems, mItemList = transfer(mUserItems, mItemDict)
    ShowUserItem(mUserItems)

if __name__ == '__main__':
    main()
    plt.show()
