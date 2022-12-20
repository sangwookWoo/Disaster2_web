import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import os
import folium
from folium.plugins import MarkerCluster
# pip install streamlit-folium 관리자권한 아나콘다
from streamlit_folium import st_folium
import datetime
from PIL import Image

filePath, fileName = os.path.split(__file__)


def TsunamiShelter():
    pageNo = 1
    numOfRows = 1000
    type = 'json'
    url = f'http://223.130.129.189:9191/getTsunamiShelter1List/numOfRows={numOfRows}&pageNo={pageNo}&type={type}'
    response = requests.get(url)
    json_ob = json.loads(response.content)
    body = json_ob['TsunamiShelter'][1]['row']
    body = pd.json_normalize(body)
    return body

def Shelter_map(data):
        m = folium.Map(
        location=[data['lat'].mean(), data['lon'].mean()],
        zoom_start= 7, width = '70%', height = '50%',  scrollWheelZoom=False, dragging=False
        )
        marker_cluster = MarkerCluster().add_to(m)
        for idx in data.index:
                text = data.loc[idx, 'shel_nm'] + '<br>상세주소 :' + data.loc[idx, 'address'] + '<br>수용 가능 인원수 :' + str(data.loc[idx, 'shel_av'])  + '<br>해변으로부터 거리 :' + str(data.loc[idx, 'lenth']) + 'M' + '<br>해발 높이 :' + str(data.loc[idx, 'height']) + '<br>내진적용여부 :' + data.loc[idx, 'seismic']
                folium.Marker([data.loc[idx, 'lat'], data.loc[idx, 'lon']], icon = folium.Icon(color="red"), tooltip = text).add_to(marker_cluster)
        return m
    
def main():
    st.set_page_config(
    page_title = "⛔위기 대응 프로젝트",
    layout = 'wide' 
    )
    st.header("🌊지진 해일 대피소 정보")
    st.write("지역을 선택하고 지도를 확대하면서, 가까운 지진해일 국내 대피소 정보를 받아보세요🙏")
    df = TsunamiShelter()
    sido_list = list(df['sido_name'].unique())
    sido_list.insert(0, '전국')
    cd_nm = st.selectbox('시도 선택',sido_list)
    if cd_nm != '전국':
        df = df[df['sido_name'] == cd_nm]
    
    m = Shelter_map(df)
    st_folium(m, returned_objects=[])

    
    
if __name__ == "__main__":
    main()