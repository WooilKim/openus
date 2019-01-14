import requests
from bs4 import BeautifulSoup as bs
import re
import sqlite3 as sql


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
    for page in range(1, 100):
        params = {'strPage': page}
        url = "http://likms.assembly.go.kr/bill/LatestReceiptBill.do"
        print(page)
        source = requests.post(url, data=params)
        plain_text = source.text
        # print(plain_text)
        soup = bs(plain_text, 'lxml')
        for title in soup.select('table > tbody > tr > td > a'):
            if not title.has_attr('href'):
                continue
            # print(title)
            # print(title.attrs['href'])
            parent = title.parent.parent
            print('의안번호', parent.contents[1].text)
            print('제안구분', parent.contents[5].text)
            print('제안일', parent.contents[7].text)
            if not parent.contents[9].contents[1].has_attr('href'):
                print('소관위', parent.contents[9].contents[1]['title'])
            else:
                print('소관위', parent.contents[9].contents[1]['title'], parent.contents[9].contents[1]['href'])

            # for c in p.contents:
            #     print(c)
            # print('회부일', parent.findNext('td').findNext('td').findNext('td').text)
            # print(parent.findNext('td').contents[1])
            # print(parent.findNext('td').contents[2])

            l = list(re.findall("\'{1}[\w\d]*\'{1}", title.attrs['href'], re.S))
            billID, opt = l[0][1:-1], l[1][1:-1]
            print(title['title'], billID, opt)
            # print(match.group(1))

            # print(title.attrs['href'].split('[\(\),]'))
            # billID = title.attrs['href'][22:-25]
            # print(billID)
            detailurl = "http://likms.assembly.go.kr/bill/billDetail.do?billId=" + billID
            detailsource = requests.get(detailurl)
            detailsoup = bs(detailsource.text, 'lxml')
            # for t in detailsoup.select('tbody > tr > td > a'):
            #     if not t.has_attr('href'):
            #         continue
            # print(t['href'])
            coactorurl = "http://likms.assembly.go.kr/bill/coactorListPopup.do?billId=" + billID
            coactorsource = requests.get(coactorurl)
            coactorsoup = bs(coactorsource.text, 'lxml')
            for c in coactorsoup.select('a'):
                # cname = re.split('\\(\\)', c.text)
                name, remain = c.text.split('(')
                party, remain = remain.split('/')
                name_chinese, _ = remain.split(')')

                print(name, party, name_chinese, c['href'][58:])
            # print(coactorsource.text)
            # http://likms.assembly.go.kr/bill/coactorListPopup.do?billId=PRC_V1Y9Y0B1F1N4V1I4M0L6V5Z0A3C4O7


# http://likms.assembly.go.kr/bill/billDetail.do?billId=PRC_V1Z9D0X1W1B0J1E7P5B9T1M6C4U5Q0
# http://likms.assembly.go.kr/bill/coactorListPopup.do?billId=PRC_V1Z9D0X1W1B0J1E7P5B9T1M6C4U5Q0
if __name__ == '__main__':
    recent_bills()
