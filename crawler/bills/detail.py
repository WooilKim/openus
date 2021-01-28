import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import json

#2100042
url = "https://likms.assembly.go.kr/bill/billDetail.do?billId=PRC_T2V0G0N6K0I1R1H6D5L5E0Q7O3T7Z9"
source = requests.post(url)
soup = bs(source.text, 'lxml')
# 의안 상세 페이지
table_dict = {}
bill_num = soup.select('table > tbody > tr > td')[0].text # 의안번호
print(bill_num)
file = soup.select('table > tbody > tr > td > a')
for href in file:
    print(href)
    l = re.findall("\'[\d]*\'{1}", href.attrs['href'], re.S)
    print(l)

"""
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


#http://likms.assembly.go.kr/filegate/servlet/FileGate?bookId=D2A2D401-9E69-4586-7A05-A82E79FBF1E7&type=0
#'http://likms.assembly.go.kr/filegate/servlet/FileGate','D2A2D401-9E69-4586-7A05-A82E79FBF1E7','0'

jsondict = json.dumps(table_dict, indent=4, ensure_ascii=False)
print(jsondict)

with open(f'./의안정리/{bill_num}.json', 'w') as f:
    f.write(jsondict)
    f.flush()

print(jsondict)
"""
