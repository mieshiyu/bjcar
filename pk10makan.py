from time import sleep
from datetime import datetime, time
import random
import re
import copy




class pk10makan():

    def __init__(self, xiadan_yk):
        """下单列表2"""
        self.xiadan_yk_l = None

        self.xiadan_gl_l = None

        self.xiadan_loss = 0

        self.xiadan_list_2 = []

        #self.xiadan_list = []

        self.xiadan_yk_list = None

        self.xiadan_hc = None

        self.MA5 = []

        self.MA5_hc = []

    def DataProcessing(self, date):
        self.date_list = ['冠军', '亚军', '季军', '第四名', '第五名',
                          '第六名', '第七名', '第八名', '第九名', '第十名']
        self.panduan_daxiao = 0
        self.panduan_daxiao_list = []
        self.panduan_danshuang = 0
        self.xiadan_list_chufa = []
        self.NO_Pmlist = [{'大小': []}, {'单双': []}]
        self.xiadan_list = []
        self.xiadan_yk_l_2 = []


        for i in self.date_list:
            self.NO_Pmlist[0]['大小'].append(date[i][2])
        for i in self.date_list:
            self.NO_Pmlist[1]['单双'].append(date[i][4])
        self.NO_Pmlist.insert(0, [date['期数'], date['日期']])
        for i in self.date_list:
            self.NO_Pmlist.append([i, date[i][1], date[i][2]])
        for i in self.date_list:
            self.NO_Pmlist.append([i, date[i][3], date[i][4]])

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
            #print(self.MA5_hc)
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
                {'单双总连现值': self.MA5_hc[-1][3]['单双均值']}
            ]
            print(self.MA5)
            del self.MA5_hc[0]
        #if self.NO_Pmlist[0]




        # if self.NO_Pmlist[1]['大小'].count(1) + self.NO_Pmlist[2]['单双'].count(1) <= 11:
        if self.NO_Pmlist[1]['大小'].count(1) >= 8:
            for i in self.NO_Pmlist[3:14]:
                if i[2] >= 7:
                    self.xiadan_list_chufa.append([self.NO_Pmlist[0], i, self.NO_Pmlist[1]['大小'].count(1)])
        elif self.NO_Pmlist[1]['大小'].count(1) >= 6:
            for i in self.NO_Pmlist[3:14]:
                if i[2] >= 10:
                    self.xiadan_list_chufa.append([self.NO_Pmlist[0], i, self.NO_Pmlist[1]['大小'].count(1)])

        if self.NO_Pmlist[2]['单双'].count(1) >= 8:
            for i in self.NO_Pmlist[15:26]:
                if i[2] >= 7:
                    self.xiadan_list_chufa.append([self.NO_Pmlist[0], i, self.NO_Pmlist[2]['单双'].count(1)])
        elif self.NO_Pmlist[2]['单双'].count(1) >= 6:
            for i in self.NO_Pmlist[15:26]:
                if i[2] >= 10:
                    self.xiadan_list_chufa.append([self.NO_Pmlist[0], i, self.NO_Pmlist[2]['单双'].count(1)])

        print(self.NO_Pmlist)
        # 1、检查是否有下单触发
        # 2、1 没有下单触发
        if self.xiadan_list_chufa == []:
            # 3、1 检查上次下单是否亏损，有亏损
            if self.xiadan_yk_list:
                self.xiadan_yk(self.xiadan_yk_list, self.NO_Pmlist)
                try:
                    for i in self.xiadan_yk_list:
                        # 4、1 亏损次数 < 3
                        if i[0] < 3:
                            # print('1')
                            self.xiadan([i])

                        # 4、2 亏损次数 = 3
                        elif i[0] == 3:
                            # print('2')
                            print('%s 已经亏损3次,无触发新的信号' % i)
                            self.xiadan_yk_list.remove(i)
                            self.xiadan(self.xiadan_yk_list)
                            self.xiadan_list_2 = []
                except:
                    self.xiadan(self.xiadan_yk_list)


            # 3、2 没有亏损
            else:
                pass

        # 2、2 有下单触发
        else:
            # 3、1 检查上次下单是否亏损，有亏损
            if self.xiadan_yk_list:
                self.xiadan_yk(self.xiadan_yk_list, self.NO_Pmlist)
                try:
                    # 4、1 亏损次数 < 3
                    for i in self.xiadan_yk_list:
                        if i[0] < 3:
                            # print('3')
                            self.xiadan([i])

                        # 4、2 亏损次数 = 3
                        elif i[0] == 3:
                            # print('4')
                            print('%s 已经亏损3次，有新的信号 %s' % (i, self.xiadan_list_chufa))
                            self.xiadan_list_2 = []
                            for i in self.xiadan_list_chufa:
                                # i[0][0:1]+i[1][0:2] = ['728060','第六名', '大', 10]
                                self.xiadan_list_2.append([0]+i[0]+i[1])
                            if self.xiadan_list_2 == []:
                                pass
                            else:
                                if len(self.xiadan_list_2) > 1:
                                    self.xiadan_list_2 = random.sample(self.xiadan_list_2, 1)
                            self.xiadan(self.xiadan_list_2)
                            self.xiadan_yk_list = copy.copy(self.xiadan_list_2)
                except:
                    self.xiadan(self.xiadan_yk_list)

            # 3、2 没有亏损，直接下单
            else:
                # print('5')
                for i in self.xiadan_list_chufa:
                    # i[0][0:1]+i[1][0:2] = ['728060','第六名', '大', 10]
                    self.xiadan_list_2.append([0]+i[0]+i[1])
                if self.xiadan_list_2 == []:
                    pass
                else:
                    if len(self.xiadan_list_2) > 1:
                        self.xiadan_list_2 = random.sample(self.xiadan_list_2, 1)
                self.xiadan(self.xiadan_list_2)
                self.xiadan_yk_list = copy.copy(self.xiadan_list_2)

    def xiadan(self, date):
        try:
            for i in date:
                # date[0][0][0:1] + date[0][1][0:2] = ['728060','第六名', '大']
                self.xiadan_list = i
                if self.xiadan_hc == i:
                    # print('无需下单2')
                    pass
                else:
                    print('下单的', self.xiadan_list, '亏损第 %s 次' % self.xiadan_list[0])
                self.xiadan_hc = copy.copy(i)
        except:
            print('无需下单')
            self.xiadan_list_2 = []

    def xiadan_yk(self, xiadan_date, date):
        NO_Pmlist = [date[0], date[3:]]
        if xiadan_date == []:
            self.xiadan_yk_l = []
        else:
            self.xiadan_yk_l = xiadan_date
        xiadan_you = 0
        if self.xiadan_yk_l:
            try:
                for i in NO_Pmlist[1]:
                    try:
                        for k in self.xiadan_yk_l:
                            if i[0:2] == k[3:5]:
                                if i[2] != 1:
                                    xiadan_you += 1
                                    if xiadan_you > 0:
                                        k[0] += 1
                                        self.xiadan_yk_l_2.append([k[0]]+NO_Pmlist[0]+i)
                                        self.xiadan_yk_list = self.xiadan_yk_l_2
                                        # print(self.xiadan_yk_list, '7')
                                    else:
                                        self.xiadan_yk_list = None
                                else:
                                    self.xiadan_yk_list = None
                            else:
                                pass
                    except EnvironmentError as e:
                        print(e)
                        #self.xiadan_yk_list = None
                        pass
            except EnvironmentError as e:
                #pass
                print(e)