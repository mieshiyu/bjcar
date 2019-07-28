from time import sleep
from datetime import datetime, time
import random
import re
import copy


#全局list
"""下单列表2"""
xiadan_l_2 = [[]]


def pk10_xiaobo(NO_pangminglist, NO_pangminglist_loss):
    global xiadan_l_2
    #先清空列表
    """方便hc缓存的列表"""
    xiadan_l_kanda = []
    xiadan_l_zhuixiao = []
    """下单列表"""
    xiadan_list_da_kan = []
    """下单列表"""
    xiadan_list_xiao_zhui = []
    """下单列表3"""
    xiadan_da_kan_yk = 0
    xiadan_xiao_zhui_yk = 0

    xiadan_kanda = []
    xiadan_zhuixiao = []

    xiadan_kanda_hc = []
    xiadan_zhuixiao_hc = []
    """下单盈亏表"""
    xiadan_yk = [0]

    xiadan_canshu = 2

    re_NO = []

    NO_MAX = 0

    #总上次列表
    for NO_one in NO_pangminglist_loss:
        re_NO.append([NO_one[0] + NO_one[1]])

    # 砍龙计算
    #选大龙
    for NO_one in NO_pangminglist:
        # print(NO_one)
        """读取排名"""
        # 要砍的高排名
        NO_MAX = max(NO_MAX, NO_one[2])

    for NO_one in NO_pangminglist:
        if NO_one[2] == NO_MAX:
            xiadan_list_da_kan.append(NO_one)

    #挑选其中之一
    if len(xiadan_list_da_kan) > 1:
        xiadan_list_da_kan = random.sample(xiadan_list_da_kan, 1)

    try:
        for i in re_NO:
            #砍成功了返回空值，失败插入失败的
            if i not in xiadan_kanda_hc:
                xiadan_kanda = []
            else:
                xiadan_kanda.append(i)
    except:
        xiadan_kanda = []

    if len(xiadan_list_da_kan) == 0:
        xiadan_l_kanda.insert(0, [])
    else:
        for i in xiadan_list_da_kan:
            re_NO = i[0] + i[1]
            xiadan_l_kanda.insert(0, re_NO)

    #缓存下单列表
    if (xiadan_kanda_hc[0]) == []:
        xiadan_da_kan_yk = ( - len(xiadan_kanda)) * xiadan_canshu
    elif (xiadan_kanda_hc[0]) != []:
        xiadan_da_kan_yk = (len(xiadan_kanda_hc) - len(xiadan_kanda)) * xiadan_canshu
    else:
        xiadan_da_kan_yk = 0
    xiadan_kanda_hc = copy.copy(xiadan_list_da_kan)



    for NO_one in NO_pangminglist:
        # print(NO_one)
        """读取排名"""
        # 要追的低排名
        if int(NO_one[2]) <= 4:
            """选择对应排名的格子"""
            xiadan_list_xiao_zhui.append(NO_one)

    #追龙计算
    try:
        # 追成功了返回成功的，失败插入空值
        if xiadan_zhuixiao_hc in re_NO:
            xiadan_zhuixiao.append(xiadan_zhuixiao_hc[0])
        elif xiadan_zhuixiao_hc not in re_NO:
            xiadan_zhuixiao = []
    except:
        xiadan_zhuixiao = []

    # 筛选下单数量 永远小于等于3
    if len(xiadan_list_xiao_zhui) > 2:
        xiadan_list_xiao_zhui = random.sample(xiadan_list_xiao_zhui, 2)

    if xiadan_zhuixiao_hc:
        xiadan_xiao_zhui_yk = (len(xiadan_list_xiao_zhui) - len(xiadan_zhuixiao)) * xiadan_canshu
    xiadan_zhuixiao_hc = copy.copy(xiadan_list_xiao_zhui)






    if len(xiadan_list) == 0:
        xiadan_l.insert(0, [])
    else:
        for i in xiadan_list:
            re_NO = i[0] + i[1]
            xiadan_l.insert(0, re_NO)

    if (xiadan_l_2[0]) == []:
        xiadan_yk.insert(0, (len(xiadan_l_2[0]) - (len(xiadan_loss)) * 2) * xiadan_canshu + xiadan_yk[0])
    elif (xiadan_l_2[0]) != []:
        xiadan_yk.insert(0, (len(xiadan_l_2) - (len(xiadan_loss)) * 2) * xiadan_canshu + xiadan_yk[0])
        #print((len(xiadan_l_2) - (len(xiadan_loss)) * 2), xiadan_l_2, '2',xiadan_loss,'loss')
    else:
        xiadan_yk.insert(0, xiadan_yk[0])
    xiadan_l_2 = copy.copy(xiadan_l)

    '''
    if xiadan_yk[0] < 0:
        if xiadan_yk[0] <= -5:
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
        
    '''

    xiadan_canshu = 2

    hh = [xiadan_canshu, xiadan_list, xiadan_loss, xiadan_yk[0]]
    return hh