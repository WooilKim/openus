import requests
from bs4 import BeautifulSoup as bs
import re
import json
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import os
import shutil
import time

age_list = ["100001", "100002", "100003", "100004", "100005", "100006", "100007", "100008", "100009", "100010",
            "100011", "100012", "100013", "100014", "100015", "100016", "100017", "100018", "100019", "100020",
            "100021"]


url = "https://open.assembly.go.kr/portal/data/service/selectServicePage.do?infId=OBL7NF0011935G18076&infSeq=1&isInfsPop=Y"
driver = webdriver.Chrome('/Users/WonyongSeo/Documents/crawling/chromedriver')
driver.get(url)

for age in age_list:
    select_age = Select(driver.find_element_by_xpath("//*[@id='sheet-filter-UNIT_CD']"))
    select_age.select_by_value(age)
    age_ = age[-2:] #대수

    folder_path = "의원/" + age_
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    # 의원 대수 선택
    driver.find_element_by_xpath("//a[@id='sheet-search-button']").click()

    # 의원 json 다운로드
    driver.find_element_by_xpath("//*[@id='sheet-json-button']").click()
    time.sleep(5)

    # json 디렉터리 변경
    src = "/Users/WonyongSeo/Downloads/"
    filename = "역대국회의원인적사항.json"
    new_path = os.getcwd() + "/의원/" + age_ + "/"
    shutil.move(src + filename, new_path + filename)
    # json load
    f = open(f"./의원/{age_}/역대국회의원인적사항.json", encoding="UTF-8")
    raw_data = json.loads(f.read())

    for i in range(1, len(raw_data)):
        index = format(i, '03')
        dict = {}
        name = raw_data[i]["HG_NM"]
        dict['이름'] = name
        dict['한문명'] = raw_data[i]["HJ_NM"]
        dict['생년월일'] = raw_data[i]["BTH_DATE"]
        dict['정당'] = raw_data[i]["POLY_NM"]
        dict['선거구'] = raw_data[i]["ORIG_NM"]
        dict['당선횟수'] = raw_data[i]["REELE_GBN_NM"]
        dict['당선대수'] = raw_data[i]["UNITS"].replace('제', '').replace('대', '')
        print(dict)
        jsondict = json.dumps(dict, indent=4, ensure_ascii=False)

        with open(f'./의원/{age_}/{index}_{name}.json', 'w') as f:
            f.write(jsondict)
            f.flush()
