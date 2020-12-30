from bs4 import BeautifulSoup as bs
import re
import requests
import json

url = "https://assembly.go.kr/assm/memact/congressman/memCond/memCondListAjax.do?currentPage=1&rowPerPage=300"

source = requests.post(url)
soup = bs(source.text, "lxml")

for tag in soup.select('.memberna_list dl'):
    dict = {}
    name = tag.find('a').text #이름

    name_han = tag.select_one('.chi').text.strip().replace('(', '').replace(')','') #한문

    id = re.search(r'\d+', tag.find('a')['href']) #id
    if id:
        id = id.group(0)
    else:
        id = None
    #print(name, name_han, id)
    dict['id'] = id
    dict['이름'] = name
    dict['한문명'] = name_han
    id_url = "https://www.assembly.go.kr/assm/memPop/memPopup.do?dept_cd=" + id
    #의원 페이지
    id_source = requests.post(id_url)
    id_soup = bs(id_source.text, "lxml")

    for tag in id_soup.select('.info_mna > ul'):
        for tag_left in tag.select('.left'):
            profile = tag_left.select('li')
            birth = profile[3].text
            dict['생년월일'] = birth #생년월일
            #print(birth)
            #print(dict)

        for tag_right in tag.select('.right > .pro_detail'):
            dd_list = []
            for dd_tag in tag_right.select('dd:nth-child(2n)'):
                dd = re.sub(r'[\s+\t\r\n]', '', dd_tag.text.strip())
                dd_list.append(dd)

            dict['정당'] = dd_list[0]
            dict['선거구'] = dd_list[1]
            dict['소속위원회'] = dd_list[2]
            dict['당선횟수'] = dd_list[3]
    print(dict)
    jsondict = json.dumps(dict, indent=4, ensure_ascii=False)
    with open(f'./의원/{name}.json', 'w') as f:
        f.write(jsondict)
        f.flush()
