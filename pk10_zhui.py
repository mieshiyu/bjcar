from time import sleep
from datetime import datetime, time
import random
import re
import copy

#全局list
"""下单列表2"""
xiadan_l_2 = [[]]

xiadan_yk = [0]

xiadan_canshu = 2

def pk10_zhui(NO_pangminglist, NO_pangminglist_loss):
    global xiadan_l_2
    global xiadan_yk
    global xiadan_canshu
    #先清空列表
    """方便l_2缓存的列表"""
    xiadan_l = []
    """下单列表"""
    xiadan_list = []
    """下单列表3"""
    xiadan_loss = []
    """下单盈亏表"""

    re_NO = []

    NO_MAX = 0
    for NO_one in NO_pangminglist:
        #print(NO_one)
        """读取排名"""
        #先遍历NO_pangminglist然后选择最大值
        NO_MAX = max(NO_MAX, NO_one[2])

    for NO_one in NO_pangminglist_loss:
        re_NO.append([NO_one[0] + NO_one[1]])
    try:
        if xiadan_l_2 in re_NO:
            xiadan_loss.insert(0, xiadan_l_2[0])
        elif xiadan_l_2 not in re_NO:
            xiadan_loss = []
    except:
        xiadan_loss = []

    for NO_one in NO_pangminglist:
        if NO_one[2] == NO_MAX:
            xiadan_list.append(NO_one)

    #处理xiadan_list 如果有多个值选择其中一个
    if len(xiadan_list) > 1:
        xiadan_list = random.sample(xiadan_list, 1)

    if len(xiadan_list) == 0:
        xiadan_l.insert(0, [])
    else:
        for i in xiadan_list:
            re_NO = i[0] + i[1]
            xiadan_l.insert(0, re_NO)

    if (xiadan_l_2[0]) == []:
        xiadan_yk.insert(0, xiadan_yk[0])
    elif (xiadan_l_2[0]) != []:
        if len(xiadan_loss) == 0:
            xiadan_yk.insert(0, - xiadan_canshu + xiadan_yk[0])
        else:
            xiadan_yk.insert(0, len(xiadan_loss) * xiadan_canshu + xiadan_yk[0])
        #print((len(xiadan_l_2) - (len(xiadan_loss)) * 2), xiadan_l_2, '2',xiadan_loss,'loss')
    else:
        xiadan_yk.insert(0, xiadan_yk[0])
    xiadan_l_2 = copy.copy(xiadan_l)


    if xiadan_yk[0] < 0:
        if xiadan_yk[0] <= -100:
            # 亏损超过5以后 一块一块打回去
            xiadan_canshu = 1
        else:
            xiadan_loss_canshu = abs(xiadan_yk[0])
            xiadan_canshu = int(xiadan_loss_canshu) + 1

    elif xiadan_yk[0] >= 0:
        """下单金额默认 2"""
        xiadan_canshu = 2
        # 把下单yk清零
        # xiadan_yk[0] = 0

    #xiadan_canshu= 2

    hh = [xiadan_canshu, xiadan_list, xiadan_loss, xiadan_yk[0]]
    return hh



