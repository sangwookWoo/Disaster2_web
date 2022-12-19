import requests
import pprint
import json
import pandas as pd
import os

filePath, fileName = os.path.split(__file__)


'''tempory house api to csv'''
def temporary_house():
    vin_df = pd.DataFrame()
    pageNo = 1
    while pageNo <= 16:
            pageNo = str(pageNo)
            url = 'http://apis.data.go.kr/1741000/TemporaryHousingFacilityVictim3/getTemporaryHousingFacilityVictim1List'
            params ={'serviceKey' : '3ouN4EKp4qGz+V76EbDHKehnbp5sYL0o19tpl5fAl2Q7s4ZosClGRfc1ENwk+2Px4QUPi4gCuCHGuG3kXFrs9w==',
                    'pageNo' : pageNo,
                    'numOfRows' : '1000',
                    'type' : 'json' }

            response = requests.get(url, params=params)
            contents = response.text
            json_ob = json.loads(contents)
            body = json_ob['TemporaryHousingFacilityVictim'][1]['row']
            body = pd.json_normalize(body)
            vin_df = pd.concat([vin_df,body], axis = 0)
            pageNo = int(pageNo) + 1
            
    columns = ['ctprvn_nm', 'sgg_nm', 'acmdfclty_se_nm', 'vt_acmdfclty_nm', 'dtl_adres', 'fclty_ar', 'vt_acmd_psbl_nmpr', 'mngps_nm', 'mngps_telno', 'xcord', 'ycord']
    vin_df2 = vin_df[columns]
    vin_df2.columns = ['시도명', '시군구명', '시설구분', '시설명', '상세주소','시설면적', '주거능력','관리부서','지자체담당자연락처', '경도', '위도']
    vin_df2.reset_index(drop = True).to_csv(os.path.join(filePath, 'pages','using_data', 'temporary_house.csv'), index = False, encoding = 'utf-8-sig')


'''save_items data process'''
def save_items(df, path):
    df = pd.read_csv(path)
    df['시도명'] = df['주소'].str.split(' ').str[0]
    df['시군구명'] = df['주소'].str.split(' ').str[1]
    df.to_csv(os.path.join(filePath, 'pages', 'using_data', '구호물자정보.csv'), index = False, encoding = 'utf-8-sig')