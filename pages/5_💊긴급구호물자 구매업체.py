import streamlit as st
import pandas as pd
import numpy as np
import os
# from streamlit_option_menu import option_menu




filePath, fileName = os.path.split(__file__)

def main():
    data_path = os.path.join(filePath,'using_data','구호물자정보.csv')

    st.set_page_config(
        page_title = "⛔위기 대응 프로젝트",
        layout = 'centered'
    )

    st.header("💊긴급구호물자 구매업체")
    st.write("위치 정보를 선택하여  \n 가까운 구매업체를 찾으세요🙏")
    df = pd.read_csv(data_path)

    cd_nm = st.selectbox('시도 선택',list(df['시도명'].unique()))
    sgg_nm = st.selectbox('시군구 선택',list(df[df['시도명'] == cd_nm]['시군구명'].unique()))
    df = df[(df['시도명'] == cd_nm) & (df['시군구명'] == sgg_nm)]
    df = df.set_index('업체명').drop(columns = ['시도명', '시군구명'])
    st.dataframe(data= df, use_container_width= True)

if __name__ == "__main__":
    main()

