import requests
from bs4 import BeautifulSoup as bs


def finished_bills():
    for page in range(1, 100):
        params = {'strPage': page}
        url = "http://likms.assembly.go.kr/bill/FinishBill.do"
        print(page)
        source = requests.post(url, data=params)
        plain_text = source.text
        # print(plain_text)
        soup = bs(plain_text, 'lxml')
        for title in soup.select('table > tbody > tr > td > a'):
            billID = title.attrs['href'][22:-16]
            print(billID)
            detailurl = "http://likms.assembly.go.kr/bill/billDetail.do?billId=" + billID
            detailsource = requests.get(detailurl)
            detailsoup = bs(detailsource.text, 'lxml')
            for t in detailsoup.select('tbody > tr > td > a'):
                print(t['href'])


def recent_bills():
    for page in range(1, 100):
        params = {'strPage': page}
        url = "http://likms.assembly.go.kr/bill/LatestReceiptBill.do"
        print(page)
        source = requests.post(url, data=params)
        plain_text = source.text
        # print(plain_text)
        soup = bs(plain_text, 'lxml')
        for title in soup.select('table > tbody > tr > td > a'):
            print(title.attrs['href'])
            print(title.attrs['href'].split('[\(\),]'))
            billID = title.attrs['href'][22:-25]
            print(billID)
            detailurl = "http://likms.assembly.go.kr/bill/billDetail.do?billId=" + billID
            detailsource = requests.get(detailurl)
            detailsoup = bs(detailsource.text, 'lxml')
            for t in detailsoup.select('tbody > tr > td > a'):
                print(t['href'])
# http://likms.assembly.go.kr/bill/billDetail.do?billId=PRC_V1Z9D0X1W1B0J1E7P5B9T1M6C4U5Q0
# http://likms.assembly.go.kr/bill/coactorListPopup.do?billId=PRC_V1Z9D0X1W1B0J1E7P5B9T1M6C4U5Q0
if __name__ == '__main__':
    # finished_bills()
    recent_bills()

