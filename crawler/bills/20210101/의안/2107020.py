import requests
from bs4 import BeautifulSoup as bs
import json

nested_dict = {}
dict, dict2 = {}, {}
url = "https://likms.assembly.go.kr/bill/billDetail.do?billId=PRC_T2Q0H1P2K2T3D1U1J4B6W2Y6B6T2N4"
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

jsondict = json.dumps(nested_dict, indent=4, ensure_ascii=False)
print(jsondict)

with open(f'./의안/{bill_num}.json', 'w') as f:
    f.write(jsondict)
    f.flush()
