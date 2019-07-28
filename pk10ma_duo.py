from time import sleep
from datetime import datetime, time
import random
import re
import copy
from time import sleep
from datetime import datetime, time

class pk10ma():
    """5条均线"""
    def __init__(self):
        pass
        # 多失败列表
        self.duo_loss = []
        # 空失败——字典
        self.kong_loss = {}         # kong_sc
        # 多赢的——字典            # duo_sc
        self.duo_win = {}
        # 空赢的列表
        self.kong_win = []
        # 多下单列表
        self.xiadan_list_duo = []
        # 空下单列表
        self.xiadan_list_kong = []
        # 下单盈亏比照列表
        self.xiadan_yk_list = []

        # 盈亏记录
        self.godlike = 0

    # --------------------------------------------------------------------------------------------

    def DataProcessing(self, NO_Pmlist, last_MA5_xiadan_duo, last_MA5_xiadan_kong,
                       MA5_dx_duo, MA5_dx_kong, MA5_s_duo, MA5_s_kong, MA_duo, MA_kong):
        # 1.0 时间过滤
        NO_Pmlist = NO_Pmlist
        trader_time = datetime.strptime(NO_Pmlist[0][1][-5:], '%H:%M')
        trader_time = trader_time.time()
        if trader_time < time(10, 00) or trader_time > time(23, 48):
            pass
        else:
            # 2.0 统计空信号失败次数
            # 2.1 生成下单盈亏比照列表
            # test ———— last_MA5_xiadan_list = ['第八名小', '第六名单', '第七名双']
            for i in NO_Pmlist[3:]:
                self.xiadan_yk_list.append(i[0]+i[1])
            # print(self.xiadan_yk_list)
            # 3.1 统计多空盈亏次数
            try:
                # 多
                for i in last_MA5_xiadan_duo:
                    if i not in self.xiadan_yk_list:
                        # 多失败记录列表
                        self.duo_loss.append(i)
                # 从多赢的字典中删除键值，并结算盈利次数
                for key in self.duo_win:
                    if key in self.duo_loss:
                        self.godlike = self.godlike + len(self.duo_win[key]) - 1
                        del self.duo_win[key]
                        self.duo_loss.remove(key)
                # 上次多赢的字典生成
                # 已存在的上次的键值
                for key in self.duo_win:
                    if key in last_MA5_xiadan_duo:
                        if self.duo_win[key][-1] == 1:
                            self.duo_win[key].append(1)
                        last_MA5_xiadan_duo.remove(key)
                # 成功连续第一次的 新建键值
                for i in last_MA5_xiadan_duo:
                    if i in self.xiadan_yk_list:
                        self.duo_win[i] = [1]

                # 空
                # 因为空要跳过一次，所以内置连续上次不清空
                if self.kong_loss != {}:
                    last_MA5_xiadan_kong = []
                    for key in self.kong_loss:
                        last_MA5_xiadan_kong.append(key)

                for i in last_MA5_xiadan_kong:
                    if i not in self.xiadan_yk_list:
                        # 空赢记录列表
                        self.kong_win.append(i)

                # 从空输的字典中 结算失败次数，并从失败字典中剔除
                for key in self.kong_loss:
                    if key in self.kong_win:
                        if self.kong_loss[key] == [1]:
                            MA_kong = MA_kong + 1
                            self.godlike = self.godlike - 1
                        elif self.kong_loss[key] == [1, 0]:
                            self.godlike = self.godlike + 1
                        del self.kong_loss[key]
                # 上次空失败的字典处理
                # self.kong_sc.append(i)
                for key in self.kong_loss:
                    if key in last_MA5_xiadan_kong:
                        # 空要识别上次位数 前次为1 这次记0 不下单，前次为0这次记1下单
                        if self.kong_loss[key][-1] == 1:
                            self.kong_loss[key].append(0)
                        else:
                            self.kong_loss[key].append(1)
                        # 移除已经有的上次记录
                        last_MA5_xiadan_kong.remove(key)
                # 上次没有的记录新建
                for i in last_MA5_xiadan_kong:
                    if i in self.xiadan_yk_list:
                        self.kong_loss[i] = [1]

                # test print(self.duo_loss, 'duo_loss', self.kong_loss, 'kong_loss')
                # 计算盈利
                # 空
                self.godlike = self.godlike + len(self.kong_win)
                self.godlike = self.godlike - len(self.duo_loss)
                # 计算亏损
                # 空
                for key in self.kong_loss:
                    if self.kong_loss[key] == [1, 0, 1]:
                        MA_kong = MA_kong + 3
                        self.godlike = self.godlike - 3
                        del self.kong_loss[key]
                # 多
                MA_duo = MA_duo + len(self.duo_loss)
            except:
                MA_duo = MA_duo
                MA_kong = MA_kong

            # 3.2 根据盈亏次数判断
            # 3.3 空失败 >= 3
            if MA_kong >= 3:
                self.kong_loss = {}
                # 4.1 多失败 >= 3
                if MA_duo >= 3:
                    self.duo_win = {}
                    self.xiadan_list_duo = []
                    self.xiadan_list_kong = []
                    # print('多空都失败3次,全天休息')
                # 4.2 多失败 <= 3
                elif MA_duo < 3:
                    # 5.1 上次多信号不为空，继续多
                    if self.duo_win != {}:
                        duo_list = []
                        for key in self.duo_win:
                            duo_list.append(key)
                        self.xiadan_list_duo = duo_list
                        duo_list = []
                    # 5.2 上次多信号为空，有新的多信号则开多，没有则等待
                    else:
                        if MA5_dx_duo[-1] == 2.5:
                            for i in NO_Pmlist[3:]:
                                if i[2] >= 7:
                                    self.xiadan_list_duo.append(i[0]+i[1])
                        elif MA5_s_duo[-1] == 2.5:
                            for i in NO_Pmlist[3:]:
                                if i[2] >= 7:
                                    self.xiadan_list_duo.append(i[0]+i[1])
                        else:
                            self.xiadan_list_duo = []
                            # print('空失败过多，多无信号，等待下次')
            # 空失败 < 3
            elif MA_kong < 3:
                # 上次空信号为空,判断当前空信号
                if self.kong_loss == {}:
                    if MA5_dx_kong[-1] < 0:
                        for i in NO_Pmlist[3:]:
                            if i[2] >= 7:
                                self.xiadan_list_kong.append(i[0]+i[1])
                    elif MA5_s_kong[-1] < 0:
                        for i in NO_Pmlist[3:]:
                            if i[2] >= 7:
                                self.xiadan_list_kong.append(i[0]+i[1])
                    # 开空后，从赢的字典中删除键值，并结算盈利次数
                    try:
                        for key in self.duo_win:
                            if key in self.xiadan_list_kong:
                                self.godlike = self.godlike + len(self.duo_win[key])
                                del self.duo_win[key]
                    except:
                        pass
                    # 没有空信号
                    else:
                        if MA_duo >= 3:
                            self.duo_win = {}
                            self.xiadan_list_duo = []
                            self.xiadan_list_kong = []
                            # print('空无信号，多失败3次,等待下期')
                        # 4.2 多失败 <= 3
                        elif MA_duo < 3:
                            # 5.1 上次多信号不为空，继续多
                            if self.duo_win != {}:
                                duo_list = []
                                for key in self.duo_win:
                                    duo_list.append(key)
                                self.xiadan_list_duo = duo_list
                                duo_list = []
                            # 5.2 上次多信号为空，有新的多信号则开多，没有则等待
                            else:
                                if MA5_dx_duo[-1] == 2.5:
                                    for i in NO_Pmlist[3:]:
                                        if i[2] >= 7:
                                            self.xiadan_list_duo.append(i[0]+i[1])
                                elif MA5_s_duo[-1] == 2.5:
                                    for i in NO_Pmlist[3:]:
                                        if i[2] >= 7:
                                            self.xiadan_list_duo.append(i[0]+i[1])
                                else:
                                    self.xiadan_list_duo = []
                                    # print('空多无信号，等待下次')

                else:
                    kong_list = []
                    if MA_kong != 0:
                        self.xiadan_list_kong = []
                    else:
                        for key in self.kong_loss:
                            if self.kong_loss[key][-1] == 0:
                                self.xiadan_list_kong = []
                            else:
                                kong_list.append(key)
                        self.xiadan_list_kong = kong_list
                        kong_list = []
                        # 开空后，从赢的字典中删除键值，并结算盈利次数
                    try:
                        for key in self.duo_win:
                            if key in self.xiadan_list_kong:
                                self.godlike = self.godlike + len(self.duo_win[key]) - 1
                                del self.duo_win[key]
                    except:
                        pass

            if len(self.xiadan_list_duo) > 3-MA_duo:
                self.xiadan_list_duo = random.sample(self.xiadan_list_duo, 3-MA_duo)
            else:
                pass
            hh = [self.xiadan_list_duo, self.xiadan_list_kong, self.godlike, MA_duo, MA_kong]
            # 清空
            self.xiadan_list_duo = []
            self.xiadan_list_kong = []
            self.xiadan_yk_list = []
            self.duo_loss = []
            self.kong_win = []
            return hh
