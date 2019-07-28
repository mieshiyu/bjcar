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
        self.MA5_xiadan_list = []
        self.last_MA5_xiadan_list = None
        # 已有参数
        # self.MA5_dx_duo = [0, 0, 0, 0, 0]
        # self.MA5_dx_kong = [0, 0, 0, 0, 0]

        # self.MA5_s_duo = [0, 0, 0, 0, 0]
        # self.MA5_s_kong = [0, 0, 0, 0, 0]

        # 总参数列表 self.NO_Pmlist

        self.last_MA5_xiadan_duo = []
        self.last_MA5_xiadan_kong = []

        self.MA_duo = 0
        self.MA_kong = 0

        # ----------------------------------------------------------------------
    def readdate(self, dateday):

        dateday = 'data/' + dateday + '.csv'
        with open(dateday) as f:
            # print('到了')
            pk10date = csv.DictReader(f)
            l = pk10ma()
            for d in pk10date:
                self.date_jisuan(d)
                self.date_huice(d)
                self.NO_pangminglist(d)
                # print(self.NO_Pmlist)
                for i in self.NO_Pmlist[1]['大小']:
                    self.zongtongji_list_dx.append(i)
                for i in self.NO_Pmlist[2]['单双']:
                    self.zongtongji_list_s.append(i)

                for i in self.NO_Pmlist[1]['大小']:
                    self.huaxian_list_dx.append(i)
                for i in self.NO_Pmlist[2]['单双']:
                    self.huaxian_list_s.append(i)
                #re，匹配日期 00：00
                self.huanxian_qishu.append(d['日期'][-5:])

                self.huaxian_7_dx.append(self.huaxian_list_dx.count(7))
                self.huaxian_8_dx.append(self.huaxian_list_dx.count(8))
                self.huaxian_9_dx.append(self.huaxian_list_dx.count(9))
                self.huaxian_10_dx.append(self.huaxian_list_dx.count(10))
                self.huaxian_11_dx.append(self.huaxian_list_dx.count(11))

                self.huaxian_one_dx.append(self.huaxian_list_dx.count(1))
                self.huaxian_he_dx.append(self.huaxian_list_dx.count(2) + self.huaxian_list_dx.count(3) + self.huaxian_list_dx.count(4) +
                                       self.huaxian_list_dx.count(5) + self.huaxian_list_dx.count(6) + self.huaxian_list_dx.count(7) +
                                       self.huaxian_list_dx.count(8) + self.huaxian_list_dx.count(9) + self.huaxian_list_dx.count(10))

                self.huaxian_7_s.append(self.huaxian_list_s.count(7))
                self.huaxian_8_s.append(self.huaxian_list_s.count(8))
                self.huaxian_9_s.append(self.huaxian_list_s.count(9))
                self.huaxian_10_s.append(self.huaxian_list_s.count(10))
                self.huaxian_11_s.append(self.huaxian_list_s.count(11))

                self.huaxian_one_s.append(self.huaxian_list_s.count(1))
                self.huaxian_he_s.append(self.huaxian_list_s.count(2) + self.huaxian_list_s.count(3) + self.huaxian_list_s.count(4) +
                                       self.huaxian_list_s.count(5) + self.huaxian_list_s.count(6) + self.huaxian_list_s.count(7) +
                                       self.huaxian_list_s.count(8) + self.huaxian_list_s.count(9) + self.huaxian_list_s.count(10))

                try:
                    self.MA5_daxiao_jun.append(self.MA5[0]['大小1连均值'])
                    # self.MA5_daxiao_x.append(self.MA5[1]['大小1连现值'])
                    self.MA5_daxiao_zjun.append(self.MA5[2]['大小总均值'])
                    self.MA5_daxiao_zx.append(self.MA5[3]['大小总现值'])

                    if self.MA5[3]['大小总现值'] - self.MA5[2]['大小总均值'] <= 0:
                        self.MA5_dx_cha.append(-0.1)
                    else:
                        self.MA5_dx_cha.append((self.MA5[3]['大小总现值'] - self.MA5[2]['大小总均值']))


                    if self.MA5_dx_cha[-1] > self.MA5_dx_cha[-2] and self.MA5_dx_cha[-2] > self.MA5_dx_cha[-3]\
                            and self.huaxian_list_dx.count(7) >= 1 and self.MA5[2]['大小总均值'] > 2.1:
                        self.MA5_dx_duo.append(2.5)
                    else:
                        self.MA5_dx_duo.append(0)

                    if self.MA5_dx_cha[-1] < 0:
                        self.MA5_dx_kong.append(-0.1)
                    else:
                        self.MA5_dx_kong.append(0)
                except:
                    pass

                try:
                    self.MA5_s_jun.append(self.MA5[4]['单双1连均值'])
                    # self.MA5_s_x.append(self.MA5[5]['单双1连现值'])
                    self.MA5_s_zjun.append(self.MA5[6]['单双总均值'])
                    self.MA5_s_zx.append(self.MA5[7]['单双总现值'])

                    if self.MA5[7]['单双总现值'] - self.MA5[6]['单双总均值'] <= 0:
                        self.MA5_s_cha.append(-0.1)
                    else:
                        self.MA5_s_cha.append((self.MA5[7]['单双总现值'] - self.MA5[6]['单双总均值']))


                    if self.MA5_s_cha[-1] > self.MA5_s_cha[-2] and self.MA5_s_cha[-2] > self.MA5_s_cha[-3]\
                            and self.huaxian_list_s.count(7) >= 1 and self.MA5[6]['单双总均值'] > 2.1:
                        self.MA5_s_duo.append(2.5)
                    else:
                        self.MA5_s_duo.append(0)

                    if self.MA5_s_cha[-1] < 0:
                        self.MA5_s_kong.append(-0.1)
                    else:
                        self.MA5_s_kong.append(0)
                except:
                    pass

                # NO_Pmlist, last_MA5_xiadan_duo, last_MA5_xiadan_kong,MA5_dx_duo, MA5_dx_kong,
                # MA5_s_duo, MA5_s_kong, MA_duo, MA_kong
                MA5_jisuan = l.DataProcessing(self.NO_Pmlist, self.last_MA5_xiadan_duo, self.last_MA5_xiadan_kong,
                                              self.MA5_dx_duo, self.MA5_dx_kong, self.MA5_s_duo, self.MA5_s_kong,
                                              self.MA_duo, self.MA_kong)
                try:
                    self.last_MA5_xiadan_duo = copy.copy(MA5_jisuan[0])
                    print(self.last_MA5_xiadan_duo)
                    self.last_MA5_xiadan_kong = copy.copy(MA5_jisuan[1])
                    self.MA_duo = MA5_jisuan[3]
                    self.MA_kong = MA5_jisuan[4]
                except:
                    pass

                # print(self.last_MA5_xiadan_duo, self.last_MA5_xiadan_kong, self.MA_duo, self.MA_kong)

                '''
                
                '''
                # print(self.MA5_dx_kong[-1], 'kong', self.MA5_dx_duo[-1], 'duo')

                self.huaxianjishu += 1

                if self.huaxian_list_dx.count(1) > 12 or self.huaxian_list_dx.count(1) < 8:
                    self.pianlidu_daxiao += 1
                if self.huaxian_list_s.count(1) > 12 or self.huaxian_list_s.count(1) < 8:
                    self.pianlidu_danshuang += 1
                self.pianlidu = self.pianlidu_danshuang + self.pianlidu_daxiao
                self.huaxian_list_dx = []
                self.huaxian_list_s = []

                #print(d)

            print(
                '总偏离度', round(self.pianlidu * 20 * 10 / int(len(self.zongtongji_list_dx) + len(self.zongtongji_list_s)), 1),'%'
                '  大小偏离度', round(self.pianlidu_daxiao * 10 * 10 / int(len(self.zongtongji_list_dx)), 1), '%'
                '  单双偏离度', round(self.pianlidu_danshuang * 10 * 10 / int(len(self.zongtongji_list_s)), 1), '%'
            )

            # 统计总连续出现数量
            print('标准1 895 ，今日进度', int((len(self.zongtongji_list_dx) + len(self.zongtongji_list_s)) * 100 / 3580), '%',
                  '| 2连: 448 | 3连: 224 | 4连: 112 | 5连: 56 |'
                  ' 6连: 28 | 7连: 14 | 8连: 7 | 9连: 3.5 |  10连: 1.75 | 11连: 1 | 3+4 = 4x2+5x2 = 336')
            print('大小列表最大值', max(self.zongtongji_list_dx),
                  '———— | 2连:', self.zongtongji_list_dx.count(2),
                  '| 3连:', self.zongtongji_list_dx.count(3),
                  '| 4连:', self.zongtongji_list_dx.count(4),
                  '| 5连:', self.zongtongji_list_dx.count(5),
                  '| 6连:', self.zongtongji_list_dx.count(6),
                  '| 7连:', self.zongtongji_list_dx.count(7),
                  '| 8连:', self.zongtongji_list_dx.count(8),
                  '| 9连:', self.zongtongji_list_dx.count(9),
                  '  | 10连:', self.zongtongji_list_dx.count(10),
                  ' ———— '
                  '3连+4连 |', self.zongtongji_list_dx.count(3) + self.zongtongji_list_dx.count(4),
                  '| 4连x2+5连x2 |', self.zongtongji_list_dx.count(4) * 2 + self.zongtongji_list_dx.count(5) * 2)
            print('单双列表最大值', max(self.zongtongji_list_s),
                  '———— | 2连:', self.zongtongji_list_s.count(2),
                  '| 3连:', self.zongtongji_list_s.count(3),
                  '| 4连:', self.zongtongji_list_s.count(4),
                  '| 5连:', self.zongtongji_list_s.count(5),
                  '| 6连:', self.zongtongji_list_s.count(6),
                  '| 7连:', self.zongtongji_list_s.count(7),
                  '| 8连:', self.zongtongji_list_s.count(8),
                  '| 9连:', self.zongtongji_list_s.count(9),
                  '  | 10连:', self.zongtongji_list_s.count(10),
                  ' ———— '
                  '3连+4连 |', self.zongtongji_list_s.count(3) + self.zongtongji_list_s.count(4),
                  '| 4连x2+5连x2 |', self.zongtongji_list_s.count(4) * 2 + self.zongtongji_list_s.count(5) * 2,
                  )

            self.pianlidu = 0

            plt.figure(1, dpi=80)
            ''''''
            x = list(range(len(self.huanxian_qishu)))
            width = 0.4
            # plt.plot(self.huanxian_qishu, self.huaxian_one_dx, 'v-', label="dx_1xian")
            # plt.plot(self.huanxian_qishu, self.huaxian_he_dx, 'v-', label="he")
            plt.bar(x, self.huaxian_7_dx, width=width, label="dx_7")
            plt.bar(x, self.huaxian_8_dx, width=width, label="dx_8")
            plt.bar(x, self.huaxian_9_dx, width=width, label="dx_9")
            plt.bar(x, self.huaxian_10_dx, width=width, label="dx_10")
            plt.bar(x, self.huaxian_11_dx, width=width, label="dx_11")

            for i in range(len(x)):
                x[i] = x[i] + width
            plt.bar(x, self.MA5_dx_kong, width=width, label="dx_kong", fc='hotpink')
            plt.bar(x, self.MA5_dx_duo, width=width, bottom=self.MA5_dx_kong, label="dx_duo", fc='y')

            plt.xticks(range(len(self.huanxian_qishu)), self.huanxian_qishu, rotation=90)
            plt.legend()
            plt.show()

            plt.figure(1, dpi=80)
            x2 = list(range(len(self.huanxian_qishu)))
            plt.bar(x2, self.huaxian_7_s, width=width, label="s_7")
            plt.bar(x2, self.huaxian_8_s, width=width, label="s_8")
            plt.bar(x2, self.huaxian_9_s, width=width, label="s_9")
            plt.bar(x2, self.huaxian_10_s, width=width, label="s_10")
            plt.bar(x2, self.huaxian_11_s, width=width, label="s_11")

            for i in range(len(x2)):
                x2[i] = x2[i] + width
            plt.bar(x2, self.MA5_s_kong, width=width, label="s_kong", fc='hotpink')
            plt.bar(x2, self.MA5_s_duo, width=width, bottom=self.MA5_s_kong, label="s_duo", fc='y')

            plt.xticks(range(len(self.huanxian_qishu)), self.huanxian_qishu, rotation=90)
            plt.legend()
            plt.show()

            # 多组数据清空列表
            self.zongtongji_list_s = []
            self.zongtongji_list_dx = []

    # ----------------------------------------------------------------------
    def date_jisuan(self, date):
        for i in self.date_list:
            date[i] = [date[i]]

            if int(date[i][0]) <= 5:
                date.setdefault(i, []).append('小')
            else:
                date.setdefault(i, []).append('大')

            if int(date[i][0]) % 2 == 0:
                date.setdefault(i, []).append('双')
            else:
                date.setdefault(i, []).append('单')

        for i in self.date_list:
            date.setdefault(i, []).insert(2, 1)
            date.setdefault(i, []).append(1)

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
        #print(date)

    # ----------------------------------------------------------------------
    def NO_pangminglist(self, date):
        self.NO_Pmlist = [{'大小': []}, {'单双': []}]
        for i in self.date_list:
            self.NO_Pmlist[0]['大小'].append(date[i][2])
        for i in self.date_list:
            self.NO_Pmlist[1]['单双'].append(date[i][4])
        self.NO_Pmlist.insert(0, [date['期数'], date['日期']])
        for i in self.date_list:
            self.NO_Pmlist.append([i, date[i][1], date[i][2]])
        for i in self.date_list:
            self.NO_Pmlist.append([i, date[i][3], date[i][4]])

        # print(self.NO_Pmlist)
        if self.NO_Pmlist[0][1][-5:] == '09:07':
            pass
        else:
            # 求大小，单双平均值
            abc = 0
            for i in range(10):
                abc += self.NO_Pmlist[1]['大小'][i]
            xiaoda_ma5 = abc/10
            bcd = 0
            for i in range(10):
                bcd += self.NO_Pmlist[2]['单双'][i]
            danshuang_ma5 = bcd / 10
            self.MA5_hc.append([{'大小': self.NO_Pmlist[1]['大小'].count(1)}, {'大小均值': xiaoda_ma5},
                               {'单双': self.NO_Pmlist[2]['单双'].count(1)}, {'单双均值': danshuang_ma5}])
        if len(self.MA5_hc) < 5:
            pass
        else:
            self.MA5 = [
                {'大小1连均值': (int(self.MA5_hc[0][0]['大小']) + int(self.MA5_hc[1][0]['大小']) +
                int(self.MA5_hc[2][0]['大小']) + int(self.MA5_hc[3][0]['大小']) + int(self.MA5_hc[4][0]['大小']))/5},
                {'大小1连现值': self.MA5_hc[-1][0]['大小']},
                {'大小总均值': (int(self.MA5_hc[0][1]['大小均值']) + int(self.MA5_hc[1][1]['大小均值']) +
                int(self.MA5_hc[2][1]['大小均值']) + int(self.MA5_hc[3][1]['大小均值'])
                          + int(self.MA5_hc[4][1]['大小均值'])) / 5},
                {'大小总现值': self.MA5_hc[-1][1]['大小均值']},
                {'单双1连均值': (int(self.MA5_hc[0][2]['单双']) + int(self.MA5_hc[1][2]['单双']) +
                int(self.MA5_hc[2][2]['单双']) + int(self.MA5_hc[3][2]['单双']) + int(self.MA5_hc[4][2]['单双'])) / 5},
                {'单双1连现值': self.MA5_hc[-1][2]['单双']},
                {'单双总均值': (int(self.MA5_hc[0][3]['单双均值']) + int(self.MA5_hc[1][3]['单双均值']) +
                          int(self.MA5_hc[2][3]['单双均值']) + int(self.MA5_hc[3][3]['单双均值'])
                          + int(self.MA5_hc[4][3]['单双均值'])) / 5},
                {'单双总现值': self.MA5_hc[-1][3]['单双均值']}
            ]
            del self.MA5_hc[0]

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
    me.readdate('2018-07-11')



