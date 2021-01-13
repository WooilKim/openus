import requests
from bs4 import BeautifulSoup as bs
from bs4 import NavigableString
from collections import defaultdict
import re
import pandas as pd
import json


url = "https://likms.assembly.go.kr/bill/billDetail.do?billId=ARC_A2V0B0A9F2I5O1O3X4N4A4O5W4X6O0"
source = requests.post(url)
soup = bs(source.text, 'lxml')

for caption in soup.find_all("caption"):
    #print(caption.text)
    if caption.text == '등록의견 리스트':
        continue
    parent = caption.parent

    dic = {}
    th_list = []
    td_list = []
    for th in parent.find_all('th'):
        th_list.append(th.text)
    print(th_list)
    for td in parent.find_all('td'):
        value = td.text.replace('\t', '').replace('\n', '').replace('\r', '').replace('\xa0', '').replace(' ', '')
        td_list.append(value)
    print(td_list)
    #d1 = zip(th_list, td_list)
    # 복수의 td목록에 대해 하나만 추가되는 상황 ex) 관련위원회 - 정무위원회, 환경노동위원회, ... > 정무위원회
    df = pd.DataFrame(columns = th_list)
    if len(td_list) > len(th_list):
        print(len(td_list), len(th_list))
        for i in range(1, int(len(td_list)/len(th_list))):
            df.loc[i] = td_list[(i-1)*len(th_list):i*len(th_list)]
    else:
        df.loc[0] = td_list



    #df = pd.(td_list)
    print(df)
    #print(dict(d1))
    """
    for i in range(len(parent.contents[5].contents[1])):
        print(parent.contents[5].contents[1].contents[i])
        print(parent.contents[7].contents[1].contents[i])
    """
    #print(parent.contents[5].contents[1].contents[2].text) #thead
    #print(parent.contents[7]) #tbody
    #print(parent)
