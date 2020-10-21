import requests
from bs4 import BeautifulSoup as bs
import re
import sqlite3 as sql
import pandas as pd
import json
from datetime import datetime


def db_init():
    conn = sql.connect('bill.db')
    cur = conn.cursor()
    cur.execute('create table recent')


def recent_bills():
    """
    http://likms.assembly.go.kr/bill/LatestReceiptBill.do 에서
    최근 접수 의안 가져오기
    """
    # conn = sql.connect('bill.db')
    # cur = conn.cursor()
    # cur.execute('create table ')
    for page in reversed(range(0, 477)):
        params = {'strPage': page}
        url = "http://likms.assembly.go.kr/bill/LatestReceiptBill.do"
        print(page)
        source = requests.post(url, data=params)
        plain_text = source.text
        # print(plain_text)
        soup = bs(plain_text, 'lxml')
        for title in soup.select('table > tbody > tr > td > a'):
            jsondict = {}
            if not title.has_attr('href'):
                continue
            # print(title)
            # print(title.attrs['href'])
            parent = title.parent.parent
            # print(parent.contents)
            bill_num = parent.contents[1].text
            print('bill_num', bill_num)
            jsondict['bill_num'] = bill_num
            # print('제안구분', parent.contents[5].text)
            # print('bill_proposed_date', parent.contents[7].text)
            jsondict['bill_proposed_date'] = parent.contents[7].text
            # print('제안회기', parent.contents[8].text)
            # if not parent.contents[9].contents[1].has_attr('href'):
            #     print('소관위', parent.contents[9].contents[1]['title'])
            # else:
            #     print('소관위', parent.contents[9].contents[1]['title'], parent.contents[9].contents[1]['href'])

            # for c in p.contents:
            #     print(c)
            # print('회부일', parent.findNext('td').findNext('td').findNext('td').text)
            # print(parent.findNext('td').contents[1])
            # print(parent.findNext('td').contents[2])

            l = list(re.findall("\'{1}[\w\d]*\'{1}", title.attrs['href'], re.S))
            billID, opt = l[0][1:-1], l[1][1:-1]
            # print(title['title'], billID, opt)
            # print('bill_title', title['title'])
            jsondict['bill_title'] = title['title']
            print('bill_id', billID)
            jsondict['bill_id'] = billID
            # print('bill_opt', opt)
            jsondict['bill_opt'] = opt
            # print(match.group(1))
            # print(title.attrs['href'].split('[\(\),]'))
            # billID = title.attrs['href'][22:-25]
            # print(billID)
            detailurl = "http://likms.assembly.go.kr/bill/billDetail.do?billId=" + billID
            detailsource = requests.get(detailurl)
            detailsoup = bs(detailsource.text, 'lxml')
            ss = detailsoup.select('div#summaryContentDiv')
            # print('summary_contents', ss[0].text.strip())
            jsondict['summary_contents'] = ss[0].text.strip()
            df = pd.read_html(
                detailurl)
            # print('df length', len(df))

            if pd.isna(df[0]['문서'][0]):
                # print('NONE')
                jsondict['doc'] = None
            else:
                # print('doc', df[0]['문서'][0])
                jsondict['doc'] = df[0]['문서'][0]
            # print('proposed', df[0]['제안회기'][0])
            jsondict['proposed_session'] = df[0]['제안회기'][0]

            if len(df) > 1:
                jsondict['others_cnt'] = len(df) - 1
                # for i in range(1, len(df)):
                #     print('others', df[i].head(5))

            # print('df', df[0].columns)
            # print('df1', df[1].columns)
            # print('df2', df[2].columns)
            # detailcontents = detailsoup.select('div.tableCol01 > tr > td > a'):
            #     if not t.has_attr('href'):
            #         continue
            # print('link', t['href'])

            # summaryContentDiv
            coactorurl = "http://likms.assembly.go.kr/bill/coactorListPopup.do?billId=" + billID
            coactorsource = requests.get(coactorurl)
            coactorsoup = bs(coactorsource.text, 'lxml')
            coactors = list()
            for c in coactorsoup.select('a'):
                # cname = re.split('\\(\\)', c.text)
                name, remain = c.text.split('(')
                party, remain = remain.split('/')
                name_chinese, _ = remain.split(')')
                # print(c['href'])
                # print(name, party, name_chinese)
                try:
                    coactors.append({'name': name, 'name_chinese': name_chinese, 'congressman_id': c['href'][-7:]})
                except:
                    coactors.append({'name': name, 'name_chinese': name_chinese, 'congressman_id': None})
            # print(name, party, name_chinese, c['href'][58:])
            jsondict['coactors'] = coactors
            jsondict['crawled_date'] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            # print(coactors)

            with open(f'./data/{bill_num}.json', 'w') as f:
                f.write(json.dumps(jsondict, indent=4, ensure_ascii=False))
                f.flush()
            # print(coactorsource.text)
            # http://likms.assembly.go.kr/bill/coactorListPopup.do?billId=PRC_V1Y9Y0B1F1N4V1I4M0L6V5Z0A3C4O7


# http://likms.assembly.go.kr/bill/billDetail.do?billId=PRC_V1Z9D0X1W1B0J1E7P5B9T1M6C4U5Q0
# http://likms.assembly.go.kr/bill/coactorListPopup.do?billId=PRC_V1Z9D0X1W1B0J1E7P5B9T1M6C4U5Q0
if __name__ == '__main__':
    recent_bills()
