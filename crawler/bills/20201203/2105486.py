import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import json

nested_dict = {}
dict, dict2, dict3, dict4, dict5, dict6, dict7 = {}, {}, {}, {}, {}, {}, {}

url = "https://likms.assembly.go.kr/bill/billDetail.do?billId=PRC_S2J0C0M9G2C4J1I0W5T1S5U8E2N2I0"
source = requests.post(url)
soup = bs(source.text, 'lxml')


bill_num = soup.select('table > tbody > tr > td')[0].text
dict['의안번호'] = bill_num
bill_date = soup.select('table > tbody > tr > td')[1].text
dict['제안일자'] = bill_date
bill_proposer = soup.select('table > tbody > tr > td')[2].text
dict['제안자'] = bill_proposer.replace('\t', '').replace('\n', '').replace('\r', '').replace('\xa0', '')
#bill_file = soup.select('table > tbody > tr > td')[3]
bill_proposed_session = soup.select('table > tbody > tr > td')[4].text
dict['제안회기'] = bill_proposed_session.replace('\t', '').replace('\n', '').replace('\r', '')
ss = soup.select('div#summaryContentDiv')
dict['제안이유 및 주요내용'] = ss[0].text.strip()
nested_dict['의안정보'] = dict

con_association = soup.select('div.contIn:nth-child(5) > div.tableCol01:nth-child(2) > table > tbody > tr > td')[0].text
dict2['소관위원회'] = con_association
sent_date = soup.select('div.contIn:nth-child(5) > div.tableCol01:nth-child(2) > table > tbody > tr > td')[1].text
dict2['회부일'] = sent_date
intro_date = soup.select('div.contIn:nth-child(5) > div.tableCol01:nth-child(2) > table > tbody > tr > td')[2].text
dict2['상정일'] = intro_date
finished_date = soup.select('div.contIn:nth-child(5) > div.tableCol01:nth-child(2) > table > tbody > tr > td')[3].text
dict2['처리일'] = finished_date
finished_result = soup.select('div.contIn:nth-child(5) > div.tableCol01:nth-child(2) > table > tbody > tr > td')[4].text
dict2['처리결과'] = finished_result
#association_file = soup.select('div.contIn:nth-child(5) > div.tableCol01:nth-child(2) > table > tbody > tr > td')[5]
nested_dict['소관위 심사정보'] = dict2

session_name = soup.select('div.contIn:nth-child(5) > div.tableCol01:nth-child(4) > table > tbody > tr > td')[0].text
dict3['회의명'] = session_name
session_date = soup.select('div.contIn:nth-child(5) > div.tableCol01:nth-child(4) > table > tbody > tr > td')[1].text
dict3['회의일'] = session_date
session_result = soup.select('div.contIn:nth-child(5) > div.tableCol01:nth-child(4) > table > tbody > tr > td')[2].text
dict3['회의결과'] = session_result
nested_dict['소관위 회의정보'] = dict3

sent_date = soup.select('div.contIn:nth-child(5) > div.tableCol01:nth-child(7) > table > tbody > tr > td')[0].text
dict4['회부일'] = sent_date
intro_date = soup.select('div.contIn:nth-child(5) > div.tableCol01:nth-child(7) > table > tbody > tr > td')[1].text
dict4['상정일'] = intro_date
finished_date = soup.select('div.contIn:nth-child(5) > div.tableCol01:nth-child(7) > table > tbody > tr > td')[2].text
dict4['처리일'] = finished_date
finished_result = soup.select('div.contIn:nth-child(5) > div.tableCol01:nth-child(7) > table > tbody > tr > td')[3].text
dict4['처리결과'] = finished_result
nested_dict['법사위 체계자구심사정보'] = dict4

session_name = soup.select('div.contIn:nth-child(5) > div.tableCol01:nth-child(9) > table > tbody > tr > td')[0].text
dict5['회의명'] = session_name
session_date = soup.select('div.contIn:nth-child(5) > div.tableCol01:nth-child(9) > table > tbody > tr > td')[1].text
dict5['회의일'] = session_date
session_result = soup.select('div.contIn:nth-child(5) > div.tableCol01:nth-child(9) > table > tbody > tr > td')[2].text
dict5['회의결과'] = session_result
nested_dict['법사위 회의정보'] = dict5

intro_date = soup.select('div.contIn:nth-child(7) > div.tableCol01:nth-child(2) > table > tbody > tr > td')[0].text
dict6['상정일'] = intro_date
decision_date = soup.select('div.contIn:nth-child(7) > div.tableCol01:nth-child(2) > table > tbody > tr > td')[1].text
dict6['의결일'] = decision_date
session_name = soup.select('div.contIn:nth-child(7) > div.tableCol01:nth-child(2) > table > tbody > tr > td')[2].text
dict6['회의명'] = session_name
session_result = soup.select('div.contIn:nth-child(7) > div.tableCol01:nth-child(2) > table > tbody > tr > td')[3].text
dict6['회의결과'] = session_result
nested_dict['본회의 심의정보'] = dict6

sent_date = soup.select('div.pr30 td')[0].text
dict7['정부이송일'] = sent_date
nested_dict['정부이송정보'] = dict7

jsondict = json.dumps(nested_dict, indent=4, ensure_ascii=False)
print(jsondict)

with open('2105486.json', 'w') as f:
    f.write(json.dumps(jsondict, indent="\t", ensure_ascii=False))
    f.flush()
