import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import json


url = "https://likms.assembly.go.kr/bill/billDetail.do?billId=PRC_N2Q0Y0W7K0K6L1S0K3N2Y1C1F4O9J7"
source = requests.post(url)
soup = bs(source.text, 'lxml')
# 의안 상세 페이지
table_dict = {}
bill_num = soup.select('table > tbody > tr > td')[0].text # 의안번호
print(bill_num)
for caption in soup.find_all("caption"): # 테이블 명 찾기
    print(caption.text)
    caption_text = caption.text
    if caption.text == '등록의견 리스트':
        continue
    parent = caption.parent

    th_list, td_list = [], []
    for th in parent.find_all('th'): # 테이블 column 찾기
        th_list.append(th.text)

    for td in parent.find_all('td'): # 테이블 내용
        value = td.text.replace('\t', '').replace('\n', '').replace('\r', '').replace('\xa0', '').replace(' ', '')
        td_list.append(value)

    df = pd.DataFrame(columns = th_list) # DataFrame화
    if len(td_list) > len(th_list): # 복수의 테이블 내용에 대해 정리
        for i in range(1, int(len(td_list)/len(th_list))):
            df.loc[i] = td_list[(i-1)*len(th_list):i*len(th_list)]
    else:
        df.loc[0] = td_list

    df_dict = df.to_dict('list')
    #print(df_dict)
    table_dict[caption_text] = df_dict

jsondict = json.dumps(table_dict, indent=4, ensure_ascii=False)
with open(f'./의안정리/{bill_num}.json', 'w') as f:
    f.write(jsondict)
    f.flush()

print(jsondict)
