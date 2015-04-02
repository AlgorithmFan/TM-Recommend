#!usr/bin/env python
#coding:utf-8

import ConfigParser
class CReadConfig:
    def __init__(self, config_file_path):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(config_file_path)

    def getBasic(self):
        day_thr = int(self.cf.get("Basic", "day_thr"))
        day_dateNum = int(self.cf.get("Basic", "day_dateNum"))
        day_interval = int(self.cf.get("Basic", "day_interval"))
        filename = self.cf.get("Basic", "filename")
        basic = {'d':(day_thr, day_dateNum, day_interval),
                 'filename': filename}
        return basic


    def getMarkov(self):
        '''得到Markov的基本配置'''
        basic = self.getBasic()
        top_num = int(self.cf.get("Markov", "top_num"))
        date_flag = self.cf.get("Markov", "date_flag")
        date_thr, date_num, date_interval = basic[date_flag]
        num_thr = self.cf.get("Markov", "num_thr")
        description = self.cf.get("Markov", "description")
        gram_n = int(self.cf.get("Markov", "gram_n"))
        filename = basic['filename']
        parameters = {'top_num':top_num, 'num_thr':num_thr, 'date_flag':date_flag,
                      'date_thr':date_thr, 'date_num': date_num, 'date_interval': date_interval,
                      'description':description, 'filename':filename, 'gram_n':gram_n}
        return parameters



if __name__ == "__main__":
    mCConfig = CReadConfig("config.ini")
    parameters = mCConfig.getMarkov()
    for key in parameters:
        print key, parameters[key]