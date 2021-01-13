import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import json


url = "https://likms.assembly.go.kr/bill/billDetail.do?billId=PRC_M2X0L0J9L1V4Z1W0L5P5A4L1X6A3M6"
source = requests.post(url)
soup = bs(source.text, 'lxml')
# 의안 상세 페이지

for caption in soup.find_all("caption"): # 테이블 명 찾기
    #print(caption.text)
    if caption.text == '등록의견 리스트':
        continue
    parent = caption.parent

    th_list = []
    td_list = []
    for th in parent.find_all('th'): # 테이블 column 찾기
        th_list.append(th.text)
    print(th_list)

    for td in parent.find_all('td'): # 테이블 내용
        value = td.text.replace('\t', '').replace('\n', '').replace('\r', '').replace('\xa0', '').replace(' ', '')
        td_list.append(value)
    print(td_list)

    df = pd.DataFrame(columns = th_list) # DataFrame화
    if len(td_list) > len(th_list):
        for i in range(1, int(len(td_list)/len(th_list))):
            df.loc[i] = td_list[(i-1)*len(th_list):i*len(th_list)]
    else:
        df.loc[0] = td_list
    print(df)

    """
    with open(f'./의안/{bill_num}.json', 'w') as f:
        f.write(jsondict)
        f.flush()
    """
