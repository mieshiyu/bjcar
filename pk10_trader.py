from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from datetime import datetime, time
import random
import re
import copy

#策略
from pk10_kan_1 import pk10_kan

class mainEngine():
    def __init__(self):
        ##进入界面
        self.browser = webdriver.Firefox()
        # 幸运
        # qqq595263944 qq20190110
        self.browser.get('https://www-xy9155.com/index.html')
        self.input_one = self.browser.find_element_by_id("guestlogin")
        self.browser.execute_script("arguments[0].click();", self.input_one)
        # 隐式等待
        sleep(5)
        # 点击确认
        self.alert = self.browser.switch_to_alert()
        sleep(2)
        self.alert.accept()
        '''
        self.browser.get('https://www-xy9155.com/index.html')
        self.input_one = self.browser.find_element_by_id("userName")
        self.input_one.send_keys('qqq595263944')
        self.input_o = self.browser.find_element_by_id("userPwd")
        self.input_o.send_keys('qq20190110')
        sleep(15)
        self.iii = self.browser.find_element_by_class_name("obt_mit")
        self.iii.click()
        '''
        sleep(15)
        self.input_two = self.browser.find_element_by_class_name("yes")
        self.input_two.click()
        sleep(10)
        self.input_a = self.browser.find_element_by_class_name("notice-btn")
        self.input_a.click()
        sleep(2)
        self.input_b = self.browser.find_element_by_class_name("notice-btn")
        self.input_b.click()
        sleep(3)
        # input_c = self.browser.find_element_by_class_name("notice-btn")
        # input_c.click()
        # sleep(5)
        # 关闭聊天室
        # input_123 = self.browser.find_element(By.XPATH, '/html/body/div[2]/div[4]/div/div/div[2]/span/a[4]/i')
        # input_123.click()

        # xiadan_time = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
        self.xiadan_time = [4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59]
        """下单列表"""
        self.xiadan_list = []
        """下单参数"""
        self.xiadan_canshu = 2
        """盈亏计数列表"""
        self.xiadan_yk = [0]
        """下单总金额"""
        self.xiadan_z = 0
        """下单休息时间"""
        self.xiadan_jishi = 0
        """xiadan_win次数"""
        self.xiadan_win = 0
        """xiadan_loss"""
        self.xiadan_loss = []
        # self.browser.switch_to_frame('framePage')

        self.trade_pk10()

    def trade_pk10(self):
        while True:
            localtime = datetime.now().time()
            self.abc = False
            if localtime <= time(23, 50):
                self.abc = True
                sleep(3)
                """判断弹窗之前先切出iframe"""
                try:
                    """如果有弹窗就点掉"""
                    self.browser.switch_to_default_content()
                    tanchuang = self.browser.find_element_by_class_name("layui-layer-title")
                    tangchuang_enter = self.alertbrowser.find_element_by_class_name("layui-layer-btn0")
                    tangchuang_enter.click()
                    print('点了个弹窗')
                except:
                    """没有弹窗进入交易"""
                    """判断是否连续失败5次加时 xiadan_jishi = 0默认为0"""
                    if int(localtime.strftime('%M')) in self.xiadan_time:
                        #print('ok')
                        sleep(23)
                        #实盘先在iframe点击刷新金额
                        #browser.switch_to_default_content()
                        #input_123 = browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[1]/ul/li[1]/div[2]/div[3]/a[2]/img')
                        #input_123.click()

                        print('----------------------------------------------------------------------')
                        """幸运的有iframe"""
                        self.browser.switch_to_frame('framePage')
                        """生成排名列表"""
                        NO_pangminglist = ((self.browser.find_element_by_class_name('u-table5')).text).split('\n')
                        """处理列表 格式化"""
                        NO_pangminglist = self.NO_pangming_list(NO_pangminglist)
                        print('排名列表为：', NO_pangminglist)

                        try:
                            pk10_celv = pk10_kan(NO_pangminglist, self.xiadan_canshu, self.xiadan_yk)
                            #策略返回 pk10_celv 格式 [xiadan_canshu, xiadan_list, xiadan_loss, xiadan_yk]
                            self.xiadan_canshu = pk10_celv[0]
                            self.xiadan_list = pk10_celv[1]
                            self.xiadan_loss = pk10_celv[2]
                            self.xiadan_yk = pk10_celv[3]


                            for i in self.xiadan_list:
                                self.paimingfenxi(i)
                                xiadan = self.browser.find_element(By.XPATH, self.paimingfenxi(i))
                                xiadan.click()
                                sleep(round(random.uniform(2, 4), 1))

                            """找到下单金额窗口"""
                            xiadan_cash = self.browser.find_element(By.XPATH, '//*[@id="bet_money2"]')
                            #清空下单金额窗口
                            xiadan_cash.clear()
                            """下单参数"""
                            self.xiadan_yk = self.xiadan_yk[0:15]
                            print(self.xiadan_yk)
                            xiadan_cash.send_keys(self.xiadan_canshu)
                            print('下注金额：', self.xiadan_canshu, '失败列表：', self.xiadan_loss)
                            print('下单个数：', len(self.xiadan_list), '下单列表：', self.xiadan_list)
                            # 清空列表
                            #self.xiadan_loss = []
                            #self.xiadan_list = []
                            sleep(5)
                            """点击确认"""
                            cash_enter = self.browser.find_element_by_id('openBetWinBtn2')
                            cash_enter.click()
                            sleep(3)
                            """弹窗点击确认 要先切换出iframe"""
                            self.browser.switch_to_default_content()
                            cash_enter = self.browser.find_element(By.XPATH, "/html/body/div[2]/div[3]/a[1]")
                            cash_enter.click()
                            """再切回去"""
                            sleep(6)
                            self.browser.switch_to_frame('framePage')

                            suiji = round(random.uniform(25, 50), 1)
                            sleep(suiji)
                            print(suiji, 's, ook', 'time：', datetime.now().time())
                        except Exception as e:
                            sleep(30)
                            print('当前列表为空,等下一期')
                            print(e)

                    else:
                        suiji2 = round(random.uniform(15, 25), 1)
                        sleep(suiji2)
                        #print(int(localtime.strftime('%M')), 'min', suiji2, 's, nno')


    def paimingfenxi(self, paiming):
        """万喜格式"""
        """冠亚和"""
        guanyahe = {
            '冠亚和大': '//*[@id="play_name_501001"]',
            '冠亚和小': '//*[@id="play_name_501002"]',
            '冠亚和单': '//*[@id="play_name_501003"]',
            '冠亚和双': '//*[@id="play_name_501004"]'
        }
        """名次"""
        mingci = {'冠军': '5011', '亚军': '5012', '第三名': '5013',
                  '第四名': '5014', '第五名': '5015',
                  '第六名': '5016', '第七名': '5017', '第八名': '5018',
                  '第九名': '5019', '第十名': '5020'
                  }

        """两面"""
        liangmian = {
            '大': '01', '小': '02', '单': '03', '双': '04', '龙': '05', '虎': '06'
        }
        """反追两面"""
        fanzhui_liangmian = {
            '大': '02', '小': '01', '单': '04', '双': '03', '龙': '06', '虎': '05'
        }
        try:
            xiadan_classname = guanyahe[(paiming[0]+paiming[1])]
            return xiadan_classname

        except:
            y1 = paiming[0]
            y2 = paiming[1]
            xiadan_classname = '//*[@id="play_name_' + mingci[y1] + fanzhui_liangmian[y2] + '"]'
            #print(xiadan_classname)
            return xiadan_classname


    def NO_pangming_list(self, NO_pangminglist):
        NO_pangminglist2 = []
        NO_pangminglist3 = []
        """格式化后插入一个新列表，方向和次数分开"""
        for i in NO_pangminglist:
            """列表2： 1去掉空格和-，2去掉第一个空格，3按空格拆分出新的列表"""
            ab = re.sub(r'\连开|\-', "", i)
            bc = re.sub(r'\s', "", ab, 1)
            dc = re.split(r' ', bc)
            NO_pangminglist2.append(dc)

        del_list = []
        for i in NO_pangminglist2:
            """要删除的列表：1去掉3连，2去掉冠亚和是小和单的，3去掉特码"""
            if int(i[2]) >= 6:
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
        """列表2和要删除的列表做差"""
        for i in NO_pangminglist2:
            if i not in del_list:
                NO_pangminglist3.append(i)
        """重新赋值后返回要交易的排名列表"""
        NO_pangminglist = NO_pangminglist3
        return NO_pangminglist


if __name__ == '__main__':
    mainEngine()
