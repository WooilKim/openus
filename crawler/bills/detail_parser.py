import requests
from bs4 import BeautifulSoup as bs
import re
import json
import pandas as pd
from datetime import date
from requests import get
import os

age_list = ["01", "02", "03", "04", "05", "AA", "06", "07", "08", "BB", "09", "10", "CC", "11", "12", "13", "14", "15",
            "16", "17", "18", "19", "20", "21"]

# parsed date
today = date.today()
date_dict = {}
date_dict['parsed_date'] = today



def load_file(age):
    f = open(f"./id_v2/{age}_id_v2.json", encoding="UTF-8")
    raw_data = json.loads(f.read())
    return raw_data


def detail_parser():
    err = []
    for age in age_list:
        raw_data = load_file(age)
        id_count = len(raw_data)
        # 저장 폴더 생성
        folder = age + "_bill_v3"
        if not os.path.exists(folder):
            os.mkdir(folder)

        for i in range(id_count):
            url = "https://likms.assembly.go.kr/bill/billDetail.do?billId=" + raw_data[i]["id"]
            source = requests.post(url)
            soup = bs(source.text, 'lxml')

            table_dict = {}
            try:
                bill_num = soup.select('table > tbody > tr > td')[0].text # 의안번호
            except: #에러 발생 시 의안 분류
                #print(raw_data[i]["의안번호"])
                error_dict = {}
                error_dict['의안번호'] = raw_data[i]["의안번호"]
                error_dict['id'] = raw_data[i]["id"]
                err.append(error_dict)
                continue
            #print(bill_num)
            for caption in soup.find_all("caption"): # 테이블 명 찾기
                #print(caption.text)
                caption_text = caption.text
                if caption.text == '등록의견 리스트':
                    continue
                parent = caption.parent

                th_list, td_list = [], []
                for th in parent.find_all('th'):  # 테이블 column 찾기
                    th_list.append(th.text)

                for td in parent.find_all('td'):  # 테이블 내용
                    value = td.text.replace('\t', '').replace('\n', '').replace('\r', '').replace('\xa0', '').replace(
                        ' ', '')
                    td_list.append(value)

                df = pd.DataFrame(columns=th_list)  # DataFrame화
                if len(td_list) > len(th_list):  # 복수의 테이블 내용에 대해 정리
                    for i in range(1, int(len(td_list) / len(th_list))):
                        df.loc[i] = td_list[(i - 1) * len(th_list):i * len(th_list)]
                else:
                    df.loc[0] = td_list

                df_dict = df.to_dict('list')
                # print(df_dict)
                table_dict[caption_text] = df_dict

            if soup.select('div#summaryContentDiv'):
                ss = soup.select('div#summaryContentDiv')
                table_dict['의안접수정보']['제안이유 및 주요내용'] = ss[0].text.strip()

            # 의안 파일 다운로드
            for a in soup.select('table > tbody > tr > td > a'):
                #print(a)
                href = a.attrs['href']

                if 'openBillFile' in href: #파일 형식 hwp, pdf 2종류
                    td = a.parent

                    k = re.findall("\'{1}(.*?)\'{1}", href)
                    #print(k)
                    fileID = k[1]
                    filetype = k[2] # 파일 형식 구분

                    file_url = "http://likms.assembly.go.kr/filegate/servlet/FileGate?bookId=" + fileID + "&type=" + filetype
                    print(file_url)

                    #파일 폴더 생성
                    file_folder = bill_num + "_file"
                    folder_path = folder + "/" + file_folder
                    if not os.path.exists(folder_path):
                        os.mkdir(folder_path)

                    if filetype == '0': # hwp 저장
                        with open(f'./{folder}/{file_folder}/{fileID}.hwp', 'wb') as f:
                            response = get(file_url)
                            f.write(response.content)
                            f.flush()
                    elif filetype == '1': # pdf 저장
                        with open(f'./{folder}/{file_folder}/{fileID}.pdf', 'wb') as f:
                            response = get(file_url)
                            f.write(response.content)
                            f.flush()

                elif 'ConfFile' in href: # pdf만 존재하는 형식
                    k = re.findall("\'{1}(.*?)\'{1}", href)
                    fileID = k[1]
                    conf_url = "http://likms.assembly.go.kr/record/new/getFileDown.jsp?CONFER_NUM="+fileID
                    print(conf_url)

                    file_folder = bill_num + "_file"
                    folder_path = folder + "/" + file_folder
                    if not os.path.exists(folder_path):
                        os.mkdir(folder_path)

                    with open(f'./{folder}/{file_folder}/{fileID}.pdf', 'wb') as f:
                        response = get(conf_url)
                        f.write(response.content)
                        f.flush()
                else:
                    continue
            #table_dict.update(date_dict)

            jsondict = json.dumps(table_dict, indent=4, ensure_ascii=False)

            # jsondict['parsed_date'] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            # print(jsondict)



            # 저장
            with open(f'./{folder}/{bill_num}_v3.json', 'w') as f:
                f.write(jsondict)
                f.flush()

            print(bill_num)

    jsonerror = json.dumps(err, indent=4, ensure_ascii=False)
    with open(f'./error_bill.json', 'w') as f:
        f.write(jsonerror)
        f.flush()

if __name__ == '__main__':
    detail_parser()
