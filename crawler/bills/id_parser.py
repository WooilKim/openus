import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import json

dict_list = []
bill_num_list = []
billID_list = []
driver = webdriver.Chrome('/Users/WonyongSeo/Documents/crawling/chromedriver')
url = "https://likms.assembly.go.kr/bill/main.do"
driver.get(url)
driver.find_element_by_xpath("//button[@class='btnSch01']").click()

select = Select(driver.find_element_by_id('pageSizeOption'))
select.select_by_visible_text('100')

for page in range(1, 75):
    driver.execute_script("GoPage({})".format(page))
    source = driver.page_source
    soup = bs(source, "lxml")
    for title in soup.select('table > tbody > tr > td > a'):
        dict = {}
        if not title.has_attr('href'):
            continue
        parent = title.parent.parent
        bill_num = parent.contents[1].text
        dict['의안번호'] = bill_num
        #bill_num_list.append(bill_num)


        l = list(re.findall("\'{1}[\w\d]*\'{1}", title.attrs['href'], re.S))
        billID = l[0][1:-1]
        dict['id'] = billID
        #billID_list.append(billID)

        dict_list.append(dict)
        print(dict)

jsondict = json.dumps(dict_list, indent=4, ensure_ascii=False)

with open(f'21st_id.json', 'w') as f:
    f.write(jsondict)
    f.flush()
