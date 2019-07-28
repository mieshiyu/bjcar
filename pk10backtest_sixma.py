import csv
import copy
#不显示科学计数法
#import numpy as np
#np.set_printoptions(suppress=True, threshold=np.nan)
import matplotlib.pyplot as plt
import re
from time import sleep
from datetime import datetime, time

#导入策略
from pk10makan import pk10makan
from pk10ma import pk10ma

########################################################################
class pk10backtext(object):
    def __init__(self):
        self.last_date = None
        self.qishu_l = []

        self.jichu_date_da_1 = 1
        self.jichu_date_da_2 = 1
        self.jichu_date_da_3 = 1
        self.jichu_date_da_4 = 1
        self.jichu_date_da_5 = 1
        self.jichu_date_da_6 = 1
        self.jichu_date_da_7 = 1
        self.jichu_date_da_8 = 1
        self.jichu_date_da_9 = 1
        self.jichu_date_da_10 = 1

        self.jichu_date_s_1 = 1
        self.jichu_date_s_2 = 1
        self.jichu_date_s_3 = 1
        self.jichu_date_s_4 = 1
        self.jichu_date_s_5 = 1
        self.jichu_date_s_6 = 1
        self.jichu_date_s_7 = 1
        self.jichu_date_s_8 = 1
        self.jichu_date_s_9 = 1
        self.jichu_date_s_10 = 1

        self.jichu_date_dict = {
            '冠军': [self.jichu_date_da_1, self.jichu_date_s_1],
            '亚军': [self.jichu_date_da_2, self.jichu_date_s_2],
            '季军': [self.jichu_date_da_3, self.jichu_date_s_3],
            '第四名': [self.jichu_date_da_4, self.jichu_date_s_4],
            '第五名': [self.jichu_date_da_5, self.jichu_date_s_5],
            '第六名': [self.jichu_date_da_6, self.jichu_date_s_6],
            '第七名': [self.jichu_date_da_7, self.jichu_date_s_7],
            '第八名': [self.jichu_date_da_8, self.jichu_date_s_8],
            '第九名': [self.jichu_date_da_9, self.jichu_date_s_9],
            '第十名': [self.jichu_date_da_10, self.jichu_date_s_10]
        }

        self.date_list = ['冠军', '亚军', '季军', '第四名', '第五名',
                          '第六名', '第七名', '第八名', '第九名', '第十名']

        self.header = ['期数', '日期', '冠军', '亚军', '季军', '第四名',
                       '第五名', '第六名', '第七名', '第八名', '第九名', '第十名']

        self.six_date_dict = {
            '冠军': [1, 3, 4, 7, 8, 10],
            '亚军': [1, 5, 6, 7, 8, 9],
            '季军': [1, 3, 4, 5, 6, 9],
            '第四名': [1, 2, 3, 4, 6, 10],
            '第五名': [2, 3, 5, 8, 9, 10],
            '第六名': [1, 2, 3, 7, 8, 10],
            '第七名': [1, 2, 5, 7, 8, 10],
            '第八名': [2, 4, 6, 7, 8, 10],
            '第九名': [1, 2, 4, 6, 7, 9],
            '第十名': [1, 2, 5, 8, 9, 10]
        }

        self.six_date_dict_2 = {
            '冠军': [1,2,3,4,5,8,'当前2','历史11',1],
            '亚军': [2,3,4,6,8,9,'当前1','历史11',0],
            '季军': [1,5,7,8,9,10,'当前4','历史12',0],
            '第四名': [1,2,3,5,6,10,'当前-2','历史11',1],
            '第五名': [1,2,3,4,8,10,'当前3','历史12',1],
            '第六名': [1,2,3,6,8,9,'当前1','历史11',1],
            '第七名': [1,3,5,6,7,9,'当前1','历史11',1],
            '第八名': [3,5,6,7,8,10,'当前-2','历史11',1],
            '第九名': [1,4,5,8,9,10,'当前1','历史11',0],
            '第十名': [1,2,3,4,9,10,'当前2','历史12',1]
        }

        self.zongtongji_list_dx = []
        self.zongtongji_list_s = []

        self.huaxian_one_dx = []   #没有连续
        self.huaxian_he_dx = []  #总连续

        self.huaxian_one_s = []   #没有连续
        self.huaxian_he_s = []  #总连续

        self.pianlidu = 0             # 每天总连续偏离度
        self.pianlidu_daxiao = 0      # 每天大小连续偏离度
        self.pianlidu_danshuang = 0   # 每天单双连续偏离度

        self.huaxian_5_dx = []
        self.huaxian_6_dx = []
        self.huaxian_7_dx = []
        self.huaxian_8_dx = []
        self.huaxian_9_dx = []
        self.huaxian_10_dx = []
        self.huaxian_11_dx = []

        self.huaxian_5_s = []
        self.huaxian_6_s = []
        self.huaxian_7_s = []
        self.huaxian_8_s = []
        self.huaxian_9_s = []
        self.huaxian_10_s = []
        self.huaxian_11_s = []

        self.huaxian_list_dx = []
        self.huaxian_list_s = []
        self.huanxian_qishu = []

        self.huaxianjishu = 0

        # 下单盈亏计算
        self.xiadan_yk = [0]

        self.xiadan_z = 0

        self.xiadan_z_l = []

        # 拆分大小 单双 计算
        self.MA5 = []

        self.MA5_hc = []

        self.MA5_daxiao_jun = [0, 0, 0, 0, 0]
        self.MA5_daxiao_x = [0, 0, 0, 0, 0]
        self.MA5_daxiao_zjun = [0, 0, 0, 0, 0]
        self.MA5_daxiao_zx = [0, 0, 0, 0, 0]

        self.MA5_dx_cha = [0, 0, 0, 0, 0]

        self.MA5_dx_duo = [0, 0, 0, 0, 0]
        self.MA5_dx_kong = [0, 0, 0, 0, 0]

        self.MA5_s_jun = [0, 0, 0, 0, 0]
        self.MA5_s_x = [0, 0, 0, 0, 0]
        self.MA5_s_zjun = [0, 0, 0, 0, 0]
        self.MA5_s_zx = [0, 0, 0, 0, 0]

        self.MA5_s_cha = [0, 0, 0, 0, 0]

        self.MA5_s_duo = [0, 0, 0, 0, 0]
        self.MA5_s_kong = [0, 0, 0, 0, 0]

        # 回测相关初始化参数
        self.zhuanle = 0


        # ----------------------------------------------------------------------
    def readdate(self, dateday):

        dateday = 'data/' + dateday + '.csv'
        with open(dateday) as f:
            # print('到了')
            pk10date = csv.DictReader(f)
            l = pk10ma()
            for d in pk10date:
                self.date_jisuan(d)
                # print(d)
            print(self.zhuanle, '获奖比率 %.1f' % (self.zhuanle*100/1790), '%')
            self.zhuanle = 0

    # ----------------------------------------------------------------------
    def date_jisuan(self, date):
        for key in self.six_date_dict:
            if int(date[key]) in self.six_date_dict[key]:
                # print(date[key], '中了')
                self.zhuanle += 1

        #self.date_huice(date)
        #print(date)

    # ----------------------------------------------------------------------
    def date_huice(self, date):
        for i in self.date_list:
            if self.last_date:
                if self.last_date[i][1] == date[i][1]:
                    self.jichu_date_dict[i][0] += 1
                    date[i][2] = self.jichu_date_dict[i][0]
                else:
                    self.jichu_date_dict[i][0] = 1
                    date[i][2] = self.jichu_date_dict[i][0]

            if self.last_date:
                if self.last_date[i][3] == date[i][3]:
                    self.jichu_date_dict[i][1] += 1
                    date[i][4] = self.jichu_date_dict[i][1]
                else:
                    self.jichu_date_dict[i][1] = 1
                    date[i][4] = self.jichu_date_dict[i][1]

        self.last_date = copy.copy(date)
    # ----------------------------------------------------------------------
    def backtest(self, NO_Pmlist, last_MA5_xiadan_list, MA5_dx_duo, MA5_dx_kong,
                 MA5_s_duo, MA5_s_kong, MA_duo, MA_kong):

        pass
        # 策略返回 pk10_celv 格式 [xiadan_canshu, xiadan_list, xiadan_loss, xiadan_yk]
        #print(l[0], l[1], l[2], l[3])
        #self.xiadan_z = l[3]
        #return self.xiadan_z  #循环N次结果用到

if __name__ == '__main__':
    # 格式'2019-01-1'
    # 标准1 1790 ，2 895 ，3 447.5 ，4 223.75 ，5 111.875 ，
    # 6 55.9375 ，7 27.96 ，8 14 ，9 7 ，10 3.5 ，11 1.75 ，12 1
    me = pk10backtext()
    for i in range(1, 32):
        day = '2018-12-' + str(i)
        print(day)
        me.readdate(day)



