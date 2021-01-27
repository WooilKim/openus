import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import json


age_list = ["01", "02", "03", "04", "05", "AA", "06", "07", "08", "BB", "09", "10", "CC", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21"]
driver = webdriver.Chrome('/Users/WonyongSeo/Documents/crawling/chromedriver')

for i in age_list:
    dict_list = []
    url = "https://likms.assembly.go.kr/bill/main.do"
    driver.get(url)

    #대수 설정
    select_agefrom = Select(driver.find_element_by_xpath("//*[@id='si1_label01']"))
    select_agefrom.select_by_value(i)

    select_ageto = Select(driver.find_element_by_xpath("//*[@id='srchForm']/div/div[1]/select[2]"))
    select_ageto.select_by_value(i)

    #검색 버튼
    driver.find_element_by_xpath("//button[@class='btnSch01']").click()
    #페이지당 보기 - 100
    select = Select(driver.find_element_by_id('pageSizeOption'))
    select.select_by_visible_text('100')

    for page in range(1, 300):
        driver.execute_script("GoPage({})".format(page))
        source = driver.page_source
        soup = bs(source, "lxml")


        for title in soup.select('table > tbody > tr > td > div > a'):
            dict = {}
            if not title.has_attr('href'):
                continue
            parent = title.parent.parent.parent
            bill_num = parent.contents[1].text
            dict['의안번호'] = bill_num

            l = list(re.findall("\'{1}[\w\d]*\'{1}", title.attrs['href'], re.S))
            billID = l[0][1:-1]
            dict['id'] = billID

            dict_list.append(dict)
            print(dict)

        for td in soup.find_all("td"): #빈 페이지 도달 시 이중루프 break
            if td.has_attr("colspan"):
                break
        else:
            continue
        break

    jsondict = json.dumps(dict_list, indent=4, ensure_ascii=False)

    with open(f'./id_v2/{i}_id_v2.json', 'w') as f:
        f.write(jsondict)
        f.flush()
