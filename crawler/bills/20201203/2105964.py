import requests
from bs4 import BeautifulSoup as bs
import json

dict = {}
url = "https://likms.assembly.go.kr/bill/billDetail.do?billId=PRC_G2W0G1K2H0I1N1Y0R1R2U0K0A9L8X8"
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

jsondict = json.dumps(dict, indent=4, ensure_ascii=False)
print(jsondict)

with open('2105964.json', 'w') as f:
    f.write(json.dumps(jsondict, indent="4", ensure_ascii=False))
    f.flush()
