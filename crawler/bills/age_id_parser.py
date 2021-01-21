import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import json

age_list = ["01", "02", "03", "04", "05", "AA", "06", "07", "08", "BB", "09", "10", "CC", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
old_age_list = ["01", "02", "03", "04", "05", "AA", "06", "07", "08", "BB", "09", "10", "CC", "11", "12", "13", "14", "15"]
recent_age_list = ["16","17","18","19","20"]
driver = webdriver.Chrome('/Users/WonyongSeo/Documents/crawling/chromedriver')

for i in old_age_list:
    dict_list = []
    url = "https://likms.assembly.go.kr/bill/main.do"
    driver.get(url)

    #대수 설정
    select_agefrom = Select(driver.find_element_by_xpath("//*[@id='si1_label01']"))
    select_agefrom.select_by_value(i)

    select_ageto = Select(driver.find_element_by_xpath("//*[@id='srchForm']/div/div[1]/select[2]"))
    select_ageto.select_by_value(i)


    driver.find_element_by_xpath("//button[@class='btnSch01']").click()
    #검색버튼 /html/body/div[1]/div[2]/div[1]/div/div[2]/form[1]/div/div[6]/button[1]
    #의안명 /html/body/div/div[2]/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/div[2]/a
    select = Select(driver.find_element_by_id('pageSizeOption'))
    select.select_by_visible_text('100')
    #select2 = Select(driver.find_element_by_id('hiddenGoDetailForm'))

    for page in range(1, 30):
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



            l = list(re.findall("\'{1}[\w\d]*\'{1}", title.attrs['href'], re.S))
            billID = l[0][1:-1]
            dict['id'] = billID

            dict_list.append(dict)
            print(dict)

    jsondict = json.dumps(dict_list, indent=4, ensure_ascii=False)

    with open(f'./id/{i}_id_v1.json', 'w') as f:
        f.write(jsondict)
        f.flush()

for i in recent_age_list:
    dict_list = []
    url = "https://likms.assembly.go.kr/bill/main.do"
    driver.get(url)

    #대수 설정
    select_agefrom = Select(driver.find_element_by_xpath("//*[@id='si1_label01']"))
    select_agefrom.select_by_value(i)

    select_ageto = Select(driver.find_element_by_xpath("//*[@id='srchForm']/div/div[1]/select[2]"))
    select_ageto.select_by_value(i)


    driver.find_element_by_xpath("//button[@class='btnSch01']").click()
    #검색버튼 /html/body/div[1]/div[2]/div[1]/div/div[2]/form[1]/div/div[6]/button[1]
    #의안명 /html/body/div/div[2]/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/div[2]/a
    select = Select(driver.find_element_by_id('pageSizeOption'))
    select.select_by_visible_text('100')
    #select2 = Select(driver.find_element_by_id('hiddenGoDetailForm'))

    for page in range(1, 300):
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



            l = list(re.findall("\'{1}[\w\d]*\'{1}", title.attrs['href'], re.S))
            billID = l[0][1:-1]
            dict['id'] = billID

            dict_list.append(dict)
            print(dict)

    jsondict = json.dumps(dict_list, indent=4, ensure_ascii=False)

    with open(f'./id/{i}_id_v1.json', 'w') as f:
        f.write(jsondict)
        f.flush()
"""
if __name__ == '__main__':
    id_parser()
"""
