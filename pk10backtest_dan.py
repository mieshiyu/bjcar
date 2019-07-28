import csv
import copy
#不显示科学计数法
#import numpy as np
#np.set_printoptions(suppress=True, threshold=np.nan)
import matplotlib.pyplot as plt
import re

#导入策略
from pk10_zhui import pk10_zhui
from pk10kan import pk10kan

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

        self.zongtongji_l = []

        self.huaxian_1 = []   #没有连续
        self.huaxian_he = []  #总连续
        self.pianlidu = 0      #每天连续偏离度

        self.huaxian_2 = []
        self.huaxian_3 = []
        self.huaxian_4 = []
        self.huaxian_5 = []
        self.huaxian_6 = []
        self.huaxian_7 = []
        self.huaxian_8 = []
        self.huaxian_9 = []
        self.huaxian_10 = []

        self.huaxian_l = []
        self.huanxian_qishu = []

        self.huaxianjishu = 0

        #下单盈亏计算
        self.xiadan_yk = [0]

        self.xiadan_z = 0

        self.xiadan_z_l = []


    # ----------------------------------------------------------------------
    def readdate(self, dateday):

        dateday = dateday + '.csv'
        with open(dateday) as f:
            # print('到了')
            pk10date = csv.DictReader(f)
            l = pk10kan(self.xiadan_yk)
            for d in pk10date:
                self.date_jisuan(d)
                self.date_huice(d)
                l.DataProcessing(d)
                for i in self.date_list:
                    self.zongtongji_l.append(d[i][2])
                    self.zongtongji_l.append(d[i][4])

                    # 生成划线np
                    self.huaxian_l.append(d[i][2])
                    self.huaxian_l.append(d[i][4])
                #re，匹配日期 00：00
                self.huanxian_qishu.append(re.findall(r'\d{1,2}\:\d{1,2}', d['日期']))

                self.huaxian_3.append(self.huaxian_l.count(3))
                self.huaxian_4.append(self.huaxian_l.count(4))
                self.huaxian_5.append(self.huaxian_l.count(5))
                self.huaxian_6.append(self.huaxian_l.count(6))
                self.huaxian_7.append(self.huaxian_l.count(7))
                self.huaxian_8.append(self.huaxian_l.count(8))
                self.huaxian_9.append(self.huaxian_l.count(9))
                self.huaxian_10.append(self.huaxian_l.count(10))

                self.huaxian_1.append(self.huaxian_l.count(1))
                self.huaxian_he.append(self.huaxian_l.count(2) + self.huaxian_l.count(3) + self.huaxian_l.count(4) +
                                       self.huaxian_l.count(5) + self.huaxian_l.count(6) + self.huaxian_l.count(7) +
                                       self.huaxian_l.count(8) + self.huaxian_l.count(9) + self.huaxian_l.count(10))


                self.huaxianjishu += 1

                if self.huaxian_l.count(1) > 12 or self.huaxian_l.count(1) < 8:
                    self.pianlidu += 1
                self.huaxian_l = []

                #print(d)

            print('偏离度', round(self.pianlidu*20*100/int(len(self.zongtongji_l)), 1), '%')
            self.pianlidu = 0

            plt.figure(1, dpi=80)
            plt.plot(self.huanxian_qishu, self.huaxian_1, 'v-', label="1")
            #plt.plot(self.huanxian_qishu, self.huaxian_he, 'o-', label="he")
            plt.plot(self.huanxian_qishu, self.huaxian_7, 'o-', label="7")
            plt.plot(self.huanxian_qishu, self.huaxian_8, 'o-', label="8")
            plt.plot(self.huanxian_qishu, self.huaxian_9, 'o-', label="9")
            plt.plot(self.huanxian_qishu, self.huaxian_10, 'o-', label="10")
            plt.xticks(self.huanxian_qishu, rotation=90)
            plt.legend()
            plt.show()

            #统计总连续出现数量
            print('标准1 1790 ，——————2: 895 ，3: 447.5 ，4: 223.75 ，5: 111.875，'
                  '6: 55.9375，7: 27.96，8: 14，9: 7，10: 3.5，11: 1.75 ，12: 1')
            print('列表最大值', max(self.zongtongji_l),
                  '今日进度', int(len(self.zongtongji_l)*100/3580), '%'
                  '  2连有', self.zongtongji_l.count(2),
                  '3连有', self.zongtongji_l.count(3),
                  '4连有', self.zongtongji_l.count(4),
                  '5连有', self.zongtongji_l.count(5),
                  '6连有', self.zongtongji_l.count(6),
                  '7连有', self.zongtongji_l.count(7),
                  '8连有', self.zongtongji_l.count(8),
                  '9连有', self.zongtongji_l.count(9),
                  '10连有', self.zongtongji_l.count(10),
                  ' ———— '
                  '3连+4连', self.zongtongji_l.count(3) + self.zongtongji_l.count(4),
                  '4连x2+5连x2', self.zongtongji_l.count(4)*2 + self.zongtongji_l.count(5)*2,
                  )

            #多组数据清空列表
            self.zongtongji_l = []


    # ----------------------------------------------------------------------
    def date_jisuan(self, date):
        for i in self.date_list:
            date[i] = [date[i]]

            if int(date[i][0]) <= 5:
                date.setdefault(i, []).append('小')
            else:
                date.setdefault(i, []).append('大')
            ''''''
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

            ''''''
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
        NO_pangminglist = date

    def backtest(self, date):

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
    me.readdate('2019-01-5')

    '''
    #循环n次测试
    for i in range(0, 10000):
        i += 1
        me.readdate('2019-01-7')
    l = me.readdate('2019-01-7')
    junzhi = 0
    for i in range(len(l)):
        junzhi += l[i]
    print('最大值', max(l), '最小值', min(l), '均值', round(junzhi/len(l), 1))
    '''


