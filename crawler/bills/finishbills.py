import requests
from bs4 import BeautifulSoup


def test():
    url = "http://likms.assembly.go.kr/bill/FinishBill.do"
    source = requests.get(url)
    plain_text = source.text
    # print(plain_text)
    soup = BeautifulSoup(plain_text, 'lxml')
    for title in soup.select('table > tbody > tr > td > a'):
        print(title)

if __name__ == '__main__':
    test()
