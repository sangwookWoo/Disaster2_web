from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import urllib
import requests
import json
import pandas as pd
from datetime import datetime,timedelta
import warnings
import xmltodict # 결과가 xml 형식으로 반환된다. 이것을 dict 로 바꿔주는 라이브러리다
import os

filePath, fileName = os.path.split(__file__)
data_path = os.path.join(filePath,'pages','using_data','기상청41_단기예보 조회서비스_오픈API활용가이드_격자_위경도(20221027).xlsx')


warnings.filterwarnings('ignore')
#초단기예보조회
#초단기예보정보를 조회하기 위해 발표일자, 발표시각, 예보지점 X 좌표, 예보지점 Y 좌표의 조회 조건으로 자료구분코드, 예보값, 발표일자, 발표시각, 예보지점 X 좌표, 예보지점 Y 좌표의 정보를 조회하는 기능
serviceKey='z5tZeY7iv8p2Ib1ApuO7q//wKERNpofeMjmWiun9zefOVRmdNnZkj9DCIiZoMTf3fhj6CEToyLj94bjSGZ4q4A==' #api 키
pageNo = '1' #페이지번호
numOfRows = '100' #한 페이지 결과 수
dataType = 'json' #요청자료형식(XML/JSON) Default: XML
base_date = '20221216' #‘22년 8월 13일 발표
base_time='1300' #06시30분 발표(30분 단위)
df=pd.read_excel(data_path)
#df['T1H','RN1','SKY','UUU','VVV','REH','PTY','LGT','VEC','WSD']=0
print(df.info())
for idx in df.index:
    nx=df.loc[idx,'격자 X']
    ny=df.loc[idx,'격자 Y']
    url = 'https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst?serviceKey={}&pageNo={}&numOfRows={}&dataType={}&base_date={}&base_time={}&nx={}&ny={}'.format(serviceKey,pageNo,numOfRows,dataType,base_date,base_time,nx,ny)
    response = requests.get(url, verify=False)
    r_data = json.loads(response.text)
    try : 
        data = pd.DataFrame(r_data['response']['body']['items']['item'])  
    except :
        data = pd.DataFrame(r_data['response']['body']['items']['item'], index = [0])
    data.drop_duplicates(['baseDate','baseTime','category'],keep='first',inplace=True,ignore_index = True)
    for j in data.index:
        df.loc[idx,data.loc[j,'category']]=data.loc[j,'fcstValue']
    print(idx)
print(df)