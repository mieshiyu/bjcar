import csv
import copy
#不显示科学计数法
#import numpy as np
#np.set_printoptions(suppress=True, threshold=np.nan)
import matplotlib.pyplot as plt
import re
from datetime import datetime, time

#导入策略
from pk10_zhui import pk10_zhui
from pk10_kan import pk10_kan

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
        self.huaxian_9 = []
        self.huaxian_10 = []

        self.huaxian_l = []
        self.huanxian_qishu = []

        self.huaxianjishu = 0

        #下单盈亏计算
        self.xiadan_yk = None

        self.xiadan_z = 0

        self.xiadan_z_l = []

        self.xiadan_zongtongji_start = {
                                    '冠军': [], '亚军': [], '季军': [], '第四名': [], '第五名': [],
                                    '第六名': [], '第七名': [], '第八名': [], '第九名': [], '第十名': []
        }
        self.xiadan_zongtongji_stop = {
                                    '冠军': [], '亚军': [], '季军': [], '第四名': [], '第五名': [],
                                    '第六名': [], '第七名': [], '第八名': [], '第九名': [], '第十名': []
        }

        self.haoma_tongji_start = {
            '冠军': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},
            '亚军': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},
            '季军': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},
            '第四名': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},
            '第五名': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},
            '第六名': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},
            '第七名': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},
            '第八名': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},
            '第九名': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},
            '第十名': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},
        }

        self.haoma_tongji_stop = {
            '冠军': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},
            '亚军': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},
            '季军': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},
            '第四名': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},
            '第五名': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},
            '第六名': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},
            '第七名': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},
            '第八名': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},
            '第九名': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},
            '第十名': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},
        }

        self.huoquzuixiao_list = {}

        self.huoquzuixiao_shibailist = {}
        # ----------------------------------------------------------------------
    def readdate(self, dateday):

        dateday = dateday + '.csv'
        with open(dateday) as f:
            # print('到了')
            pk10date = csv.DictReader(f)

            start = 1
            stop = 0
            for d in pk10date:
                self.date_int(d)
                self.time_riqichaifen(d)
                self.time_tongji(d, start, stop)
                #self.date_jisuan(d)
                #self.date_huice(d)
                #self.NO_pangminglist(d)
            #print(self.xiadan_zongtongji_start)
            self.haoma_tongji(self.xiadan_zongtongji_start, self.haoma_tongji_start)
            self.haoma_tongji(self.xiadan_zongtongji_stop, self.haoma_tongji_stop)
            #print(self.haoma_tongji_stop)
            #print(self.haoma_tongji_start)
            self.huoquzuixiao(self.haoma_tongji_start)
            print(self.huoquzuixiao_list)
            self.shibai_stop(self.haoma_tongji_stop,self.huoquzuixiao_list)
            print(self.huoquzuixiao_shibailist)
            '''
                for i in self.date_list:
                    self.zongtongji_l.append(d[i][2])
                    self.zongtongji_l.append(d[i][4])

                    # 生成划线np
                    self.huaxian_l.append(d[i][2])
                    self.huaxian_l.append(d[i][4])
                #re，匹配日期 00：00
                self.huanxian_qishu.append(re.findall(r'\d{1,2}\:\d{1,2}', d['日期']))
                self.huaxian_9.append(self.huaxian_l.count(9))
                self.huaxian_3.append(self.huaxian_l.count(3))
                self.huaxian_4.append(self.huaxian_l.count(4))
                self.huaxian_5.append(self.huaxian_l.count(5))
                self.huaxian_6.append(self.huaxian_l.count(6))
                self.huaxian_7.append(self.huaxian_l.count(7))

                self.huaxian_1.append(self.huaxian_l.count(1))
                self.huaxian_he.append(self.huaxian_l.count(2) + self.huaxian_l.count(3) + self.huaxian_l.count(4) +
                                       self.huaxian_l.count(5) +self.huaxian_l.count(6) + self.huaxian_l.count(7) +
                                       self.huaxian_l.count(8) +self.huaxian_l.count(9) + self.huaxian_l.count(10))


                self.huaxianjishu += 1

                if self.huaxian_l.count(1) > 12 or self.huaxian_l.count(1) < 8:
                    self.pianlidu += 1
                self.huaxian_l = []

            #print('偏离度', round(self.pianlidu*20*100/int(len(self.zongtongji_l)), 1), '%')
            self.pianlidu = 0

            #多个日期取最终合计值
            #print(self.xiadan_z)
            #self.xiadan_z = 0

            '''
            '''
            #循环N次结果用到
            self.xiadan_z_l.append(self.xiadan_z)
            self.xiadan_z = 0           
            return self.xiadan_z_l
            '''
            '''
            #print(self.huaxian_3)


            plt.figure(1, dpi=80)
            plt.plot(self.huanxian_qishu, self.huaxian_1, 'o-', label="1")
            plt.plot(self.huanxian_qishu, self.huaxian_he, 'o-', label="he")
            plt.xticks(self.huanxian_qishu, rotation=90)
            plt.legend()
            #plt.show()

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
            '''

    # ----------------------------------------------------------------------
    def date_int(self, date):
        for i in self.date_list:
            date[i] = int(date[i])
        #print(date)

    # ----------------------------------------------------------------------
    def time_riqichaifen(self, date):
        date['time'] = date['日期'][-5:]
    # ----------------------------------------------------------------------
    def time_tongji(self, date, start, stop):
        start = start
        stop = stop
        time_riqi = (datetime.strptime(date['time'], '%H:%M').time())
        #print(date)
        # start 76期，stop 103期 ，低于11期都可以做
        # 124  54  低于 6
        if time_riqi >= time(9,00) and time_riqi <= time(15, 30):
            for i in self.date_list:
                self.xiadan_zongtongji_start[i].insert(0, date[i])
        if time_riqi >= time(15, 30):
            for i in self.date_list:
                self.xiadan_zongtongji_stop[i].insert(0, date[i])

    # ----------------------------------------------------------------------
    def haoma_tongji(self, date, yaotongji_list):
        for i in self.date_list:
            yaotongji_list[i][1] = date[i].count(1)
            yaotongji_list[i][2] = date[i].count(2)
            yaotongji_list[i][3] = date[i].count(3)
            yaotongji_list[i][4] = date[i].count(4)
            yaotongji_list[i][5] = date[i].count(5)
            yaotongji_list[i][6] = date[i].count(6)
            yaotongji_list[i][7] = date[i].count(7)
            yaotongji_list[i][8] = date[i].count(8)
            yaotongji_list[i][9] = date[i].count(9)
            yaotongji_list[i][10] = date[i].count(10)

    # ----------------------------------------------------------------------
    def huoquzuixiao(self,date):
        #遍历每个字典排名
        for i in self.date_list:
            zuixiao = min(date[i].values())
            for (key, value) in date[i].items():
                if value == zuixiao:
                    self.huoquzuixiao_list[i] = {key: value}

    # ----------------------------------------------------------------------
    def shibai_stop(self, date, shibaizhi):
        n = 0
        for i in self.date_list:
            for (key, value) in date[i].items():
                if key in shibaizhi[i]:
                    if value >= 12:
                        n -= 1
                        self.huoquzuixiao_shibailist[i] = [{key: value}, n]
                    else:
                        self.huoquzuixiao_shibailist[i] = {key: value}


    # ----------------------------------------------------------------------
    def NO_pangminglist(self, date):
        NO_pangminglist = []

        NO_pangminglist2 = []
        NO_pangminglist3 = []
        NO_pangminglist_loss = []
        for i in self.date_list:
            NO_pangminglist2.append([i, date[i][1], date[i][2]])
        for i in self.date_list:
            NO_pangminglist2.append([i, date[i][3], date[i][4]])
        #print(NO_pangminglist)
        del_list = []
        panduan = 0
        for i in NO_pangminglist2:
            """要删除的列表：1去掉3连，2去掉冠亚和是小和单的，3去掉特码"""
            if int(i[2]) == 1:
                panduan += 1

            if int(i[2]) >= 6:
                del_list.append(i)
            if int(i[2]) <= 2:
                del_list.append(i)
            if i[1] == '龙':
                del_list.append(i)
            if i[1] == '虎':
                del_list.append(i)
            if '冠亚和' in i:
                    del_list.append(i)
            try:
                if type(int(i[1])) == int:
                    del_list.append(i)
            except:
                pass

        for i in NO_pangminglist2:
            """插入失败列表"""
            NO_pangminglist_loss.append(i)

        """列表2和要删除的列表做差"""
        for i in NO_pangminglist2:
            if i not in del_list:
                NO_pangminglist3.append(i)
        """重新赋值后返回要交易的排名列表"""
        NO_pangminglist = NO_pangminglist3

        if panduan >= 14 or panduan <= 6:
            #print('偏差过大，仅返回失败列表')
            NO_pangminglist = []
        panduan = 0

        '''
        for i in self.date_list:
            NO_pangminglist.append([i, date[i][1], date[i][2]])
        for i in self.date_list:
            NO_pangminglist.append([i, date[i][3], date[i][4]])
        '''

        self.backtest(NO_pangminglist, NO_pangminglist_loss)


    def backtest(self,date,lossdate):
        l = pk10_kan(date,lossdate)
        # 策略返回 pk10_celv 格式 [xiadan_canshu, xiadan_list, xiadan_loss, xiadan_yk]
        print(l[0], l[1], l[2], l[3])
        if self.xiadan_yk:
            self.xiadan_z += self.xiadan_yk
                #print('合计', self.xiadan_z)
        self.xiadan_yk = l[3]
        #return self.xiadan_z  #循环N次结果用到

if __name__ == '__main__':
    # 格式'2019-01-1'
    # 标准1 1790 ，2 895 ，3 447.5 ，4 223.75 ，5 111.875 ，
    # 6 55.9375 ，7 27.96 ，8 14 ，9 7 ，10 3.5 ，11 1.75 ，12 1
    me = pk10backtext()
    '''
    l = ['2019-01-1', '2019-01-2', '2019-01-3', '2019-01-4', '2019-01-5', '2019-01-6',
         '2019-01-7', '2019-01-8', '2019-01-9', '2019-01-10', '2019-01-11', '2019-01-12',
         '2019-01-13', '2019-01-14', '2019-01-15', '2019-01-16', '2019-01-17', '2019-01-18',
         '2019-01-19', '2019-01-20', '2019-01-21', '2019-01-22']
    for i in l:
        print(i, '的数据')
        me.readdate(i)
    '''

    me.readdate('2019-01-11')

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


