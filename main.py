import streamlit as st
from PIL import Image
import exchange_rate    # 모듈이름


# 사이드바 화면
st.sidebar.header("로그인")
user_id = st.sidebar.text_input('아이디(ID) 입력', value="streamlit", max_chars=15)
user_password = st.sidebar.text_input('패스워드(Password) 입력', value="", type="password")

if user_password == '1234':

    st.sidebar.header("루나의 포트폴리오")
    # selectbox_options = ['진주 귀걸이를 한 소녀', '별이 빛나는 밤', '절규', '생명의 나무', '월하정인'] # 셀렉트 박스의 선택 항목
    # your_option = st.sidebar.selectbox('좋아하는 작품은?', selectbox_options, index=0) # 셀렉트박스의 항목 선택 결과
    # st.sidebar.write('**당신의 선택**:', your_option)

    menu = st.sidebar.radio("메뉴 선택",['환율 조회','부동산 조회(EDA)','인공지능 예측/분류'],index=None)

    if menu == '환율 조회':
        exchange_rate.exchange_main()
        st.sidebar.write('환율 조회')
    elif menu == '부동산 조회(EDA)':
        st.sidebar.write('부동산 조회(EDA)')
    elif menu == '인공지능 예측/분류':
        st.sidebar.write('인공지능 예측/분류')
    else:
        st.sidebar.write('메뉴 선택해 주세요.')


    # 메인(Main) 화면
    

   