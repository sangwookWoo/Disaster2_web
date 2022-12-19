import requests
import pprint
import json
import pandas as pd

url = 'http://apis.data.go.kr/1741000/NSIService/getFcltsCheckResultInfoSearch'
params ={'serviceKey' : '3ouN4EKp4qGz+V76EbDHKehnbp5sYL0o19tpl5fAl2Q7s4ZosClGRfc1ENwk+2Px4QUPi4gCuCHGuG3kXFrs9w==',
        'pageNo' : '1',
        'numOfRows' : '10',
        'resultType' : 'json',
        'check_year' : '2020',
        'fclts_nm' : '어린이집',
        'ldong_addr_mgpl_dg_cd' : '41',
        'ldong_addr_mgpl_sggu_cd' : '41195',
        'ldong_addr_mgpl_sggu_emd_cd' : '41195000',
        'last_modf_dt' : '20200101' }

response = requests.get(url, params=params)
contents = response.text
# pp = pprint.PrettyPrinter(indent =4)
# pp.pprint(response.content)

json_ob = json.loads(contents)
body = json_ob['response']['body']['item']
body = pd.json_normalize(body)