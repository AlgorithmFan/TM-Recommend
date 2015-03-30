#!usr/bin/env python
#coding:utf-8

import ConfigParser
class CReadConfig:
    def __init__(self, config_file_path):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(config_file_path)

    def getBasic(self):
        day_dateNum = int(self.cf.get("Basic", "day_dateNum"))
        day_interval = int(self.cf.get("Basic", "day_interval"))
        basic = {'d':(day_dateNum, day_interval)}
        return basic


    def getKatzCWT(self):
        '''得到LinkAnalysis的基本配置'''
        basic = self.getBasic()
        top_num = int(self.cf.get("KatzCWT", "top_num"))
        items_thr = int(self.cf.get("KatzCWT", "items_thr"))
        date_flag = self.cf.get("KatzCWT", "date_flag")
        date_thr, date_num, date_interval = basic[date_flag]
        description = self.cf.get("KatzCWT", "description")
        theta = float(self.cf.get("KatzCWT", "theta"))
        beta = float(self.cf.get("KatzCWT", "beta"))
        parameters = {'top_num':top_num, 'items_thr':items_thr, 'date_flag':date_flag,
                      'date_thr':date_thr, 'date_num': date_num, 'date_interval': date_interval,
                      'description':description, 'theta':theta, 'beta':beta}
        return parameters

    def getPopular(self):
        '''得到LinkAnalysis的基本配置'''
        basic = self.getBasic()
        top_num = int(self.cf.get("Popular", "top_num"))
        items_thr = int(self.cf.get("Popular", "items_thr"))
        date_flag = self.cf.get("Popular", "date_flag")
        date_thr, date_num, date_interval = basic[date_flag]
        description = self.cf.get("Popular", "description")
        parameters = {'top_num':top_num, 'items_thr':items_thr, 'date_flag':date_flag,
                      'date_thr':date_thr, 'date_num': date_num, 'date_interval': date_interval,
                      'description':description}
        return parameters

    def getUBCF(self):
        basic = self.getBasic()
        top_num = int(self.cf.get("UB_CF", "top_num"))
        items_thr = int(self.cf.get("UB_CF", "items_thr"))
        date_flag = self.cf.get("UB_CF", "date_flag")
        date_num, date_interval = basic[date_flag]
        description = self.cf.get("UB_CF", "description")
        parameters = {'top_num':top_num, 'items_thr':items_thr, 'date_flag':date_flag,
                      'date_num': date_num, 'date_interval': date_interval,
                      'description':description}
        return parameters

    def getHMM(self):
        basic = self.getBasic()
        top_num = int(self.cf.get("HMM", "top_num"))
        items_thr = int(self.cf.get("HMM", "items_thr"))
        date_flag = self.cf.get("HMM", "date_flag")
        init_weight = float(self.cf.get("HMM", "init_weight"))
        trans_weight =  float(self.cf.get("HMM", "trans_weight"))
        theta_weight = float(self.cf.get("HMM", "theta_weight"))
        date_thr, date_num, date_interval = basic[date_flag]
        description = self.cf.get("HMM", "description")
        parameters = {'top_num':top_num, 'items_thr':items_thr, 'date_flag':date_flag,
                      'init':init_weight, 'trans': trans_weight, 'theta':theta_weight,
                      'date_thr':date_thr, 'date_num': date_num, 'date_interval': date_interval,
                      'description':description}
        return parameters

    def getHSMM(self):
        basic = self.getBasic()
        top_num = int(self.cf.get("HSMM", "top_num"))
        items_thr = int(self.cf.get("HSMM", "items_thr"))
        date_flag = self.cf.get("HSMM", "date_flag")
        init_weight = float(self.cf.get("HSMM", "init_weight"))
        trans_weight =  float(self.cf.get("HSMM", "trans_weight"))
        theta_weight = float(self.cf.get("HSMM", "theta_weight"))
        duration_weight = float(self.cf.get("HSMM", "duration_weight"))
        date_thr, date_num, date_interval = basic[date_flag]
        duration_max = int(self.cf.get("HSMM", "duration_max"))
        description = self.cf.get("HSMM", "description")
        parameters = {'top_num':top_num, 'items_thr':items_thr, 'date_flag':date_flag,
                      'init':init_weight, 'trans': trans_weight, 'theta':theta_weight,'duration':duration_weight,
                      'date_thr':date_thr, 'date_num': date_num, 'date_interval': date_interval,
                      'duration_max':duration_max, 'description':description}
        return parameters



if __name__ == "__main__":
    mCConfig = CReadConfig("config.ini")
    parameters = mCConfig.getUBCF()
    print type(parameters['top_num'])
    print type(parameters['items_thr'])
    print type(parameters['date_flag'])
    print parameters['date_thr']
    print parameters['date_num']
    print parameters['description']