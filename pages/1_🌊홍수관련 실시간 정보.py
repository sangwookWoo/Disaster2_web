import streamlit as st
import pandas as pd
import numpy as np
import requests
import pprint
import json
import os
import folium
from folium.plugins import MarkerCluster
# pip install streamlit-folium 관리자권한 아나콘다
from streamlit_folium import st_folium
from datetime import datetime, timedelta
from PIL import Image

filePath, fileName = os.path.split(__file__)


def flowsiteAPI_data(serviceKey, HydroType, DataType, DocumentType):
        url = f'https://api.hrfco.go.kr/{serviceKey}/{HydroType}/{DataType}{DocumentType}'
        response = requests.get(url)
        contents = response.text
        json_ob = json.loads(contents)
        body = json_ob['content']
        body = pd.json_normalize(body)
        return body
    

def flowsiteAPI_livedata(serviceKey, HydroType, DataType, DocumentType):
        url = f'https://api.hrfco.go.kr/{serviceKey}/{HydroType}/{DataType}/10M{DocumentType}'
        response = requests.get(url)
        contents = response.text
        pp = pprint.PrettyPrinter(indent =4)
        # pp.pprint(response.content)
        json_ob = json.loads(contents)
        body = json_ob['content']
        # body = json_ob['response']['body']['item']
        body = pd.json_normalize(body)
        return body
    
     
def flowsiteAPI_livedata_1h(serviceKey, HydroType, DataType, DocumentType):
        url = f'https://api.hrfco.go.kr/{serviceKey}/{HydroType}/{DataType}/1H{DocumentType}'
        response = requests.get(url)
        contents = response.text
        pp = pprint.PrettyPrinter(indent =4)
        # pp.pprint(response.content)
        json_ob = json.loads(contents)
        body = json_ob['content']
        # body = json_ob['response']['body']['item']
        body = pd.json_normalize(body)
        return body

 
def flowsite():
    serviceKey = 'A3A7BEB0-361E-4134-878C-BD8004204558'
    HydroType = 'waterlevel'
    DataType = 'list'
    DocumentType = '.json'
    water_level_live = flowsiteAPI_livedata(serviceKey, HydroType, DataType, DocumentType)
    DataType = 'info'
    water_level = flowsiteAPI_data(serviceKey, HydroType, DataType, DocumentType)
    water_level = water_level[water_level['attwl'] != ' ']
    water_level['시도명'] = water_level['addr'].str.split(' ').str[0]
    water_level['lat'] = water_level['lat'].apply(lambda x : int(x.split('-')[0]) + (int(x.split('-')[1]) / 60) + (int(x.split('-')[2]) / 3600) if len(x.split('-')) == 3 else x)
    water_level['lon'] = water_level['lon'].apply(lambda x : int(x.split('-')[0]) + (int(x.split('-')[1]) / 60) + (int(x.split('-')[2]) / 3600) if len(x.split('-')) == 3 else x)
    data = pd.merge(water_level, water_level_live, on = 'wlobscd', how = 'inner')
    data = data[data['almwl'] != ' ']
    data[['attwl', 'wrnwl', 'almwl', 'srswl', 'wl']] = data[['attwl', 'wrnwl', 'almwl', 'srswl', 'wl']].astype('float64')
    data['수위경보'] = data.apply(lambda x : '심각 수위 단계' if x['wl'] >= x['srswl']
                                                        else ('경보수위 단계' if x['wl'] >= x['almwl']
                                                        else ('주의보수위 단계' if x['wl'] >= x['wrnwl']
                                                        else ('관심수위 단계' if x['wl'] >= x['attwl'] else '정상수위 단계')))  , axis = 1)
    return data


def flow_map(data):
    m = folium.Map(
    location=[data['lat'].mean(), data['lon'].mean()],
    zoom_start= 7, width = '70%', height = '50%',  scrollWheelZoom=False, dragging=False
    )
    coords = data[['lat', 'lon', 'obsnm', '수위경보', 'pfh', 'wl']]

    # marker_cluster = MarkerCluster().add_to(m)
    for idx in coords.index:
        if coords.loc[idx,'수위경보'] == "정상수위 단계":
            folium.Marker([coords.loc[idx, 'lat'], coords.loc[idx, 'lon']], icon = folium.Icon(color="green"), tooltip = coords.loc[idx,'obsnm']  +  '<br>현재 수위 :' + str(coords.loc[idx,'wl']) + '<br>최대 수위 :' + str(coords.loc[idx,'pfh'])).add_to(m)
        elif coords.loc[idx,'수위경보'] == "관심수위 단계":
            folium.Marker([coords.loc[idx, 'lat'], coords.loc[idx, 'lon']], icon = folium.Icon(color="blue"), tooltip = coords.loc[idx,'obsnm']  +  '<br>현재 수위 :' + str(coords.loc[idx,'wl']) + '<br>최대 수위 :' + str(coords.loc[idx,'pfh'])).add_to(m)
        elif coords.loc[idx,'수위경보'] == "주의보수위 단계":
            folium.Marker([coords.loc[idx, 'lat'], coords.loc[idx, 'lon']], icon = folium.Icon(color="orange"), tooltip = coords.loc[idx,'obsnm']  +  '<br>현재 수위 :' + str(coords.loc[idx,'wl']) + '<br>최대 수위 :' + str(coords.loc[idx,'pfh'])).add_to(m)
        elif coords.loc[idx,'수위경보'] == "경보수위 단계":
            folium.Marker([coords.loc[idx, 'lat'], coords.loc[idx, 'lon']], icon = folium.Icon(color="purple"), tooltip = coords.loc[idx,'obsnm']  +  '<br>현재 수위 :' + str(coords.loc[idx,'wl']) + '<br>최대 수위 :' + str(coords.loc[idx,'pfh'])).add_to(m)
        elif coords.loc[idx,'수위경보'] == "심각수위 단계":
            folium.Marker([coords.loc[idx, 'lat'], coords.loc[idx, 'lon']], icon = folium.Icon(color="red"), tooltip = coords.loc[idx,'obsnm']  +  '<br>현재 수위 :' + str(coords.loc[idx,'wl']) + '<br>최대 수위 :' + str(coords.loc[idx,'pfh'])).add_to(m)
    return m

 
def rainfall_api():
    serviceKey = 'A3A7BEB0-361E-4134-878C-BD8004204558'
    HydroType = 'rainfall'
    DataType = 'list'
    DocumentType = '.json'
    water_level_live = flowsiteAPI_livedata(serviceKey, HydroType, DataType, DocumentType)
    DataType = 'info'
    water_level = flowsiteAPI_data(serviceKey, HydroType, DataType, DocumentType)
    water_level['시도명'] = water_level['addr'].str.split(' ').str[0]
    water_level['lat'] = water_level['lat'].apply(lambda x : int(x.split('-')[0]) + (int(x.split('-')[1]) / 60) + (int(x.split('-')[2]) / 3600) if len(x.split('-')) == 3 else x)
    water_level['lon'] = water_level['lon'].apply(lambda x : int(x.split('-')[0]) + (int(x.split('-')[1]) / 60) + (int(x.split('-')[2]) / 3600) if len(x.split('-')) == 3 else x)
    rainfall_df = pd.merge(water_level, water_level_live, on = 'rfobscd', how = 'inner')
    return rainfall_df

 
def rainfall_map(data):
    m = folium.Map(
    location=[data['lat'].mean(), data['lon'].mean()],
    zoom_start= 7
    )
    coords = data[['lat', 'lon', 'obsnm', 'rf']]
    for idx in coords.index:
        folium.Marker([coords.loc[idx, 'lat'], coords.loc[idx, 'lon']], icon = folium.Icon(color="green"), tooltip = coords.loc[idx,'obsnm'] + ' : ' + str(coords.loc[idx,'rf'])).add_to(m)
    return m

 
def dam_data_make():
        serviceKey = 'A3A7BEB0-361E-4134-878C-BD8004204558'
        HydroType = 'dam'
        DataType = 'list'
        DocumentType = '.json'
        livedata = flowsiteAPI_livedata_1h(serviceKey, HydroType, DataType, DocumentType)
        DataType = 'info'
        data = flowsiteAPI_data(serviceKey, HydroType, DataType, DocumentType)
        dam_data = pd.merge(data, livedata, on = 'dmobscd', how = 'inner')
        dam_data = dam_data[dam_data['lat'] != ' ']
        dam_data = dam_data[dam_data['lon'] != ' ']
        dam_data['lat'] = dam_data['lat'].apply(lambda x : int(x.split('-')[0]) + (int(x.split('-')[1]) / 60) + (int(x.split('-')[2]) / 3600) if len(x.split('-')) == 3 else x)
        dam_data['lon'] = dam_data['lon'].apply(lambda x : int(x.split('-')[0]) + (int(x.split('-')[1]) / 60) + (int(x.split('-')[2]) / 3600) if len(x.split('-')) == 3 else x)
        return dam_data

 
def dam_map(data):
        m = folium.Map(
        location=[data['lat'].mean(), data['lon'].mean()],
        zoom_start= 7, width = '70%', height = '50%', scrollWheelZoom=False, dragging=False
        )
        coords = data[['lat', 'lon', 'obsnm', 'swl', 'inf', 'sfw', 'ecpc', 'tototf']]
        for idx in coords.index:
                text = coords.loc[idx,'obsnm']+ '<br>현재 수위 :' + str(coords.loc[idx,'swl']) + '<br>유입량 :' + str(coords.loc[idx,'inf'])+ '<br>저수량 :' + str(coords.loc[idx,'sfw']) + '<br>공용량 :' + str(coords.loc[idx,'ecpc']) + '<br>총 방류량 :' + str(coords.loc[idx,'tototf'])
                folium.Marker([coords.loc[idx, 'lat'], coords.loc[idx, 'lon']], icon = folium.Icon(color="green"), tooltip = text).add_to(m)
        return m

 
def bo_data_make():
        serviceKey = 'A3A7BEB0-361E-4134-878C-BD8004204558'
        HydroType = 'bo'
        DataType = 'list'
        DocumentType = '.json'
        livedata = flowsiteAPI_livedata_1h(serviceKey, HydroType, DataType, DocumentType)
        DataType = 'info'
        data = flowsiteAPI_data(serviceKey, HydroType, DataType, DocumentType)
        bo_data = pd.merge(data, livedata, on = 'boobscd', how = 'inner')
        bo_data = bo_data[bo_data['lat'] != ' ']
        bo_data = bo_data[bo_data['lon'] != ' ']
        bo_data['lat'] = bo_data['lat'].apply(lambda x : int(x.split('-')[0]) + (int(x.split('-')[1]) / 60) + (int(x.split('-')[2]) / 3600) if len(x.split('-')) == 3 else x)
        bo_data['lon'] = bo_data['lon'].apply(lambda x : int(x.split('-')[0]) + (int(x.split('-')[1]) / 60) + (int(x.split('-')[2]) / 3600) if len(x.split('-')) == 3 else x)
        return bo_data

 
def bo_map(data):
        m = folium.Map(
        location=[data['lat'].mean(), data['lon'].mean()],
        zoom_start= 7, width = '70%', height = '50%',  scrollWheelZoom=False, dragging=False
        )
        coords = data[['lat', 'lon', 'obsnm', 'swl', 'inf', 'sfw', 'ecpc', 'tototf']]
        for idx in coords.index:
                text = coords.loc[idx,'obsnm']+ '<br>현재 수위 :' + str(coords.loc[idx,'swl']) + '<br>유입량 :' + str(coords.loc[idx,'inf'])+ '<br>저수량 :' + str(coords.loc[idx,'sfw']) + '<br>공용량 :' + str(coords.loc[idx,'ecpc']) + '<br>총 방류량 :' + str(coords.loc[idx,'tototf'])
                folium.Marker([coords.loc[idx, 'lat'], coords.loc[idx, 'lon']], icon = folium.Icon(color="purple"), tooltip = text).add_to(m)
        return m


def main():
    # 페이지 기본 설정
    st.set_page_config(
    page_title = "⛔위기 대응 프로젝트",
    layout = 'centered'
    )

    st.header("🌊홍수관련 실시간 정보")
    st.write("위치 정보를 선택하여 가까운 관측소 실시간 정보를 받아보세요🙏")
    
    st.markdown("###### 지도가 표시되지 않는다면 시도 선택을 다시 시도해주세요.")



    tab1, tab2, tab3 = st.tabs(["🌊실시간 수위 정보", '🏞️실시간 댐 정보', '🏞️실시간 보 정보'])
    with tab1:
        
        cd_nm = st.selectbox('시도 선택',['전국','강원도', '충청북도', '경상북도', '경기도', '서울특별시', '충청남도', '대구광역시', '경상남도',
                                            '전라북도', '부산광역시', '울산광역시', '대전광역시', '세종특별자치시', '전라남도', '광주광역시',
                                            '전남'])
        with st.spinner('정보 조회 중입니다. 잠시 기다려주세요.'):
            # 수위 데이터 조회
            data = flowsite()
            
            # 지역별 수위 데이터
            if cd_nm == "전국":
                data = data
            else :
                data = data[data['시도명'] == cd_nm]
            
            # 수위 데이터 시각화
            map = flow_map(data)
            st_folium(map, returned_objects=[])
            image = Image.open(os.path.join(filePath,'using_data','수위.png'))
            st.markdown("###### 마커 색별 수위 정보")
            st.image(image, caption=None, width=None, use_column_width=None)
            st.write(f"현재 {(datetime.now()+ timedelta(hours = 9)).strftime('%Y-%m-%d %H:%M:%S')} 기준, 10분 단위로 최신 업데이트 된 정보입니다. 해당 페이지는 한강홍수통제소의 데이터를 사용합니다😊")


    with tab2:
        with st.spinner('정보 조회 중입니다. 잠시 기다려주세요.'):
            if st.button("전국 댐 정보보기 클릭"):
                dam_data = dam_data_make()
                m = dam_map(dam_data)
                st_folium(m , returned_objects=[])
                st.write(f"현재 {(datetime.now()+ timedelta(hours = 9)).strftime('%Y-%m-%d %H:%M:%S')} 기준, 1시간 단위로 최신 업데이트 된 정보입니다. 해당 페이지는 한강홍수통제소의 데이터를 사용합니다😊")
                
    with tab3:
        with st.spinner('정보 조회 중입니다. 잠시 기다려주세요.'):
            if st.button("전국 보 정보보기 클릭"):
                bo_data = bo_data_make()
                m = bo_map(bo_data)
                st_folium(m, returned_objects=[])
                st.write(f"현재 {(datetime.now()+ timedelta(hours = 9)).strftime('%Y-%m-%d %H:%M:%S')} 기준, 1시간 단위로 최신 업데이트 된 정보입니다. 해당 페이지는 한강홍수통제소의 데이터를 사용합니다😊")
                
if __name__ == "__main__":
    main()