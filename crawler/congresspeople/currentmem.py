import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time


def current_mem():
    """
    http://likms.assembly.go.kr/bill/LatestReceiptBill.do 에서
    최근 접수 의안 가져오기
    """
    # conn = sql.connect('bill.db')
    # cur = conn.cursor()
    # cur.execute('create table ')
    # http: // www.assembly.go.kr / assm / memact / congressman / memCond / memCond.do
    driver = webdriver.Chrome('/Users/wooil/chromedriver')

    page = 1
    params = {"s_poly_cd": "",
              "s_dept_cd": "",
              "s_dtl_no": "",
              "s_elected_method": "",
              "s_up_orig_cd": "",
              "s_dw_orig_cd": "",
              "s_mem_nm": "", 'currentPage': page * 6 + 1, 'movePageNum:': '', 'rowPerPage': 6}

    # params = {}
    url = "http://www.assembly.go.kr/assm/memact/congressman/memCond/memCond.do"
    driver.get(url)
    driver.implicitly_wait(3)
    for page in range(2, 51):
        print(page)

        list = driver.find_element_by_class_name('memberna_list')
        print(list.text)
        paging = driver.find_element_by_class_name('pageing')
        span = paging.find_element_by_tag_name('span').find_elements_by_tag_name('a')
        if page % 10 == 1:
            tmp = paging.find_elements_by_tag_name('a')
            tmp[-2].click()
            time.sleep(1)
            page += 1
            list = driver.find_element_by_class_name('memberna_list')
            print(list.text)
            paging = driver.find_element_by_class_name('pageing')
            span = paging.find_element_by_tag_name('span').find_elements_by_tag_name('a')

        # if page == 11:
        #     print()
        for a in span:
            if int(a.text) == page:
                a.click()
                time.sleep(1)
                break
                # driver.implicitly_wait(100)

        #
        # print(page)
        # # source = requests.post(url, data=params)
        #
        # source = requests.get(url,params=params)
        # plain_text = source.text
        # # print(plain_text)
        # soup = bs(plain_text, 'lxml')
        # print(soup.find('div', {'id': 'listArea'}))
        # for title in soup.find('div', {'class': 'memberna_list'}):
        #     # if not title.has_attr('alt'):
        #     #     continue
        #
        #     print(title)
        #     # print(coactorsource.text)
        # http://likms.assembly.go.kr/bill/coactorListPopup.do?billId=PRC_V1Y9Y0B1F1N4V1I4M0L6V5Z0A3C4O7


# http://likms.assembly.go.kr/bill/billDetail.do?billId=PRC_V1Z9D0X1W1B0J1E7P5B9T1M6C4U5Q0
# http://likms.assembly.go.kr/bill/coactorListPopup.do?billId=PRC_V1Z9D0X1W1B0J1E7P5B9T1M6C4U5Q0
if __name__ == '__main__':
    current_mem()
