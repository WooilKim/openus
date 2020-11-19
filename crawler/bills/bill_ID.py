import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import openpyxl as xl
#from urllib.request import urlopen as uReq

bill_num_list = []
billID_list = []

for page in range(1, 561):
    params = {'strPage': page}
    url = "http://likms.assembly.go.kr/bill/LatestReceiptBill.do"
    print(page)
    source = requests.post(url, data=params)
    plain_text = source.text
    soup = bs(plain_text, 'lxml')

    for title in soup.select('table > tbody > tr > td > a'):

        if not title.has_attr('href'):
            continue
        parent = title.parent.parent
        bill_num = parent.contents[1].text
        #print(bill_num)
        bill_num_list.append(bill_num)
        l = list(re.findall("\'{1}[\w\d]*\'{1}", title.attrs['href'], re.S))
        billID = l[0][1:-1]
        #print(billID)
        billID_list.append(billID)

#print(bill_num_list)
#print(billID_list)

di = {'bill_num' : bill_num_list, 'billID' : billID_list}

df = pd.DataFrame(di, columns = ['bill_num', 'billID'])
df.sort_values(by = 'bill_num')

print(df)

df.to_excel('/Users/WonyongSeo/Desktop/21st.xlsx', sheet_name = 'SHEET', index = False)
