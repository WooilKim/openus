import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select


dict_list = []
bill_num_list = []
billID_list = []
driver = webdriver.Chrome('/Users/WonyongSeo/Documents/crawling/chromedriver')
url = "https://likms.assembly.go.kr/bill/main.do"
driver.get(url)
driver.find_element_by_xpath("//button[@class='btnSch01']").click()
#검색버튼 /html/body/div[1]/div[2]/div[1]/div/div[2]/form[1]/div/div[6]/button[1]
#의안명 /html/body/div/div[2]/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/div[2]/a
#select = Select(driver.find_element_by_xpath("//*[@id='pageSizeOption']"))
select = Select(driver.find_element_by_id('pageSizeOption'))
select.select_by_visible_text('100')
#select2 = Select(driver.find_element_by_id('hiddenGoDetailForm'))
#select2 = Select(driver.find_element_by_name("strPage"))
#select2 = Select(driver.find_element_by_xpath("/html/body/div/div[2]/form/input[39]"))
#select2.select_by_value('2')
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
"""
di = {'bill_num' : bill_num_list, 'billID' : billID_list}
df = pd.DataFrame(di, columns = ['bill_num', 'billID'])
df.sort_values(by = 'bill_num')

print(df)

df.to_excel('/Users/WonyongSeo/Desktop/21st.xlsx', sheet_name = 'SHEET', index = False)
"""
