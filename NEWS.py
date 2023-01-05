import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import requests
import json
import os
from PIL import Image
filePath, fileName = os.path.split(__file__)

def flood_news(HydroType, DataType,Edt, DocumentType):
        url = f'http://223.130.129.189:9191/{HydroType}/{DataType}/{Edt}{DocumentType}'
        response = requests.get(url)
        contents = response.text
        json_ob = json.loads(contents)
        body = json_ob['content']
        body = pd.json_normalize(body)
        return body

def main():
    try :
        # 페이지 기본 설정
        st.set_page_config(
            page_title = "⛔위기 대응 프로젝트",
            layout = 'wide'
        )

        #### 페이지 헤더, 서브헤더 제목 설정
        # 헤더
        st.header("⛔홍수 특보 발령사항")

        HydroType = 'getFldfct'
        DataType = 'list'
        # Edt = '20220810'
        DocumentType = '.json'
        Edt = datetime.today().strftime(("%Y%m%d"))
        df = flood_news(HydroType, DataType, Edt, DocumentType).drop(columns = 'links')
        df.columns = ['발표일시','발표자','수위도달 예상일시', '예상 수위표수위', '예상 해발수위', '홍수예보 종류', '홍수예보 번호', '지점', '기존발령일시', 
                    '비고','강명','변동상황', '현재 일시', '현재 수위표수위', '현재 해발수위', '예상 일시(변동)', '예상 수위표수위(변동)', '예상 해발수위(변동)', '관측소 코드', '주의 지역', 
                    '주의 강명']

        list_ = []
        for idx in df.index:
            if df.loc[idx,'홍수예보 종류'][-2:] == '발령':
                list_.append(df.loc[idx, '주의 지역'])
        warning_message = ",".join(list_)
        st.subheader("❗" + warning_message)
        st.write("해당 지역 거주자 분들은  \n  혹시 모를 사태에 대비해주시기 바랍니다.")
        df = df.set_index(['지점', '홍수예보 종류'])
        # df[['홍수예보 종류', '강명', '변동상황', '주의지역', '주의강명']]
        st.dataframe(df)
        
        image = Image.open(os.path.join(filePath,'pages','using_data', '홍수발생시 요령.png'))
        st.image(image)
        st.video('https://www.youtube.com/watch?v=cOQEdUBpLjg')
    except :
        st.write("최근 24시간 내 발효된 홍수 특보 발령사항이 없습니다😊")
        image = Image.open(os.path.join(filePath,'pages','using_data', '홍수발생시 요령.png'))
        # st.image(image)
        st.video('https://www.youtube.com/watch?v=cOQEdUBpLjg')
        st.write("해당 페이지는 웹 환경에 최적화되어 제작되었습니다.")
        pass

if __name__ == "__main__":
    main()