import requests
from bs4 import BeautifulSoup as bs
import re
import json
import pandas as pd
from datetime import date
import os

age_list = ["01", "02", "03", "04", "05", "AA", "06", "07", "08", "BB", "09", "10", "CC", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
#parsed date
today = date.today()

def load_file(age):
    f = open(f"./id/{age}_id_v1.json", encoding="UTF-8")
    raw_data = json.loads(f.read())
    return raw_data

def detail_parser():
    for age in age_list:
        raw_data = load_file(age)
        id_count = len(raw_data)

        for i in range(id_count):
            url = "https://likms.assembly.go.kr/bill/billDetail.do?billId=" + raw_data[i]["id"]
            source = requests.post(url)
            soup = bs(source.text, 'lxml')

            table_dict = {}
            bill_num = soup.select('table > tbody > tr > td')[0].text # 의안번호
            #print(bill_num)
            for caption in soup.find_all("caption"): # 테이블 명 찾기
                #print(caption.text)
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

            if soup.select('div#summaryContentDiv'):
                ss = soup.select('div#summaryContentDiv')
                table_dict['의안접수정보']['제안이유 및 주요내용'] = ss[0].text.strip()


            jsondict = json.dumps(table_dict, indent=4, ensure_ascii=False)

            #jsondict['parsed_date'] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            print(jsondict)

            # 저장 폴더 생성
            folder = age + "_bill"
            if not os.path.exists(folder):
                os.mkdir(folder)

            # 저장
            with open(f'./{age}_bill/{bill_num}_{today}_v1.json', 'w') as f:
                f.write(jsondict)
                f.flush()

            print(bill_num)


if __name__ == '__main__':
    detail_parser()
