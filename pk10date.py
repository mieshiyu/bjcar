import requests
from bs4 import BeautifulSoup
import csv
from time import time, sleep
import random

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Cookie': 'U_TRS1=000000eb.c54d4263.5847cde5.31a356b1; vjuids=-2b52c13c0.158d9fa85e6.0.422e4c7f38ffa8; vjlast=1493036659.1493914018.10; UOR=www.baidu.com,finance.sina.com.cn,; ULV=1481274492619:1:1:1::; lxlrtst=1493192605_o; lxlrttp=1495782688; SGUID=1485929373982_83888864; VISITED_FUTURE=M0_1%2Chf_NID_0%2CCU0_1%2CP1709_1%2CRU1709_1%2Chf_GC_0; FINA_V_S_2=sh600401,sz000977; SCF=AiGEM9CIAGG8O4oQ24AGltF209eufGQavTmlM5pY7ZtJngLMK1CemXupAOhHJdnZoA9Z5OnbgBgILgHgemU_puQ.; SINAGLOBAL=113.13.81.28_1487330317.221241; SUB=_2AkMv8GMuf8NhqwJRmP4XxGnlaoR-yQrEieKZrJL1JRMyHRl-yD83qmU_tRAb3voOHu_M0_EwNSjb3kUyQ_vWOQ..; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhoV73IzEndFXfDuM0u8c5d; FIN_ALL_VISITED=M0%2CNID%2Csh600401%2CCU0%2CP1709%2CRU1709; SR_SEL=1_511'
}


def downdate(urlday):
    #urlday = '2019-01-9'
    url = 'http://23.252.161.89:8666/pk10/kaijiang?date=' + urlday +'&_=1547187063603'
    response = requests.get(url, headers=headers)
    bs = BeautifulSoup(response.text, 'html.parser')
    start = time()
    print(urlday, '正在下载')
    lujing = 'data/' + urlday + '.csv'

    shuju_list = []

    header = ['期数', '日期', '冠军', '亚军', '季军', '第四名',
              '第五名', '第六名', '第七名', '第八名', '第九名', '第十名']
    #n = 1
    with open(lujing, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()


    for tr in bs.find('table', id='history').find('tbody').find_all('tr'):
        peroid = tr.find_all('td')[0].find('i').text
        date = tr.find_all('td')[0].find_all('i')[1].text
        #print(peroid, date)
        d = {
                '期数':  peroid, '日期': date,
                '冠军': tr.find_all('span')[0].text,
                '亚军': tr.find_all('span')[1].text,
                '季军': tr.find_all('span')[2].text,
                '第四名': tr.find_all('span')[3].text,
                '第五名': tr.find_all('span')[4].text,
                '第六名': tr.find_all('span')[5].text,
                '第七名': tr.find_all('span')[6].text,
                '第八名': tr.find_all('span')[7].text,
                '第九名': tr.find_all('span')[8].text,
                '第十名': tr.find_all('span')[9].text
        }

        shuju_list.insert(0, d)

    i = 0
    for i in range(0, len(shuju_list)):
        d = shuju_list[i]
        i += 1

        with open(lujing, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writerow(d)

    print(urlday, '下载完成,耗时：%s' % (time()-start))
    slp_i = round(random.uniform(3, 5), 1)
    sleep(slp_i)
    print('点击伪装时间：', slp_i)



if __name__ == '__main__':
    '''
    #下载当天
    downdate('2018-11-30')
    '''
    for i in range(14, 22):
        downdate('2018-02-' + str(i))
