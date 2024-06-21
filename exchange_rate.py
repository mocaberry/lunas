import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO

# 데이터 크롤링 함수 1 
def get_exchange_rate_data(currency_code, last_page_num):
    # base_url = "https://finance.naver.com/marketindex/exchangeDailyQuote.naver"
    df = pd.DataFrame()
    
    for page_num in range(1, last_page_num+1):
        url = f"https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_{currency_code}KRW&page={page_num}"
        dfs = pd.read_html(url, header=1,encoding='cp949')
        
        # 없어도 상관없지만, 통화 코드가 잘못 지정됐거나 마지막 페이지의 경우 for 문을 빠져나옴
        if dfs[0].empty:
            if (page_num==1):
                print(f"통화 코드({currency_code})가 잘못 지정됐습니다.")
            else:
                print(f"{page_num}가 마지막 페이지입니다.")
            break
            
        # page별로 가져온 DataFrame 데이터 연결
        df = pd.concat([df, dfs[0]], ignore_index=True)
        time.sleep(0.1) # 0.1초간 멈춤
        
    return df
# -----------------------------------------------------------------------------

# 함수 2
def exchange_main():
    st.subheader("환율 정보를 가져오는 웹 앱")
    #딕셔너리로 통화정보 만들기
    currency_name_dict = {'미국 달러':'USD','유렵연합 유로':'EUR', '일본 엔(100)':'JPY'}

    # 콤보상자 작성
    currency_name = st.selectbox("통화선택",currency_name_dict.keys())
    clicked = st.button("환율 데이터 가져오기")

    select_currency_code = currency_name_dict[currency_name]
    last_page = 10   # 변수 안에 넣어서 사용하는 습관

    if clicked:                 #데이터프레임으로 꾸렸을 때 동적 기능(다운, 서치, 넓이 조정) 가능
        # 환율코드 크롤링
        df_exchange = get_exchange_rate_data(select_currency_code, last_page)

        
        # 원하는 열만 선택
        df_exchange_rate = df_exchange[['날짜','매매기준율','사실 때','파실 때','보내실 때','받으실 때']]

        df_exchange_rate = df_exchange_rate.set_index(['날짜'])  # 날짜가 인덱스로 설정됨

        # 환율 데이터 표시
        st.dataframe(df_exchange_rate)

        #챠트 그리기(선 그래프, 판다스 이용)   인덱스가 X축 
        df_exchange_rate_2 = df_exchange_rate.copy()
        df_exchange_rate_2.index = pd.to_datetime(df_exchange_rate_2.index)

        # streamlit 에 쓸거니깐 변수 사용
        ax = df_exchange_rate_2['매매기준율'].plot(grid=True,figsize=(15,5))
        ax.set_title("Exchange Rate Graph", fontsize = 15)
        ax.set_ylabel('won/{select_currency_code}')
        
        fig = ax.get_figure()   # 차트 객체로 반드시 변환 먼저
        st.pyplot(fig)

        # 파일 다운로드
        st.subheader("== 환율 데이터 다운로드 ==")
        csv_data = df_exchange_rate.to_csv()   # () 파일 이름을 적지 않으면 가상 메모리에 기억이 됨

        # 엑셀 데이터 변환
        excel_data = BytesIO()   # 메모리 버퍼에 바이너리 객체 생성
        df_exchange_rate.to_excel(excel_data)   #컨버터 한 것을 excel_data에 넣겠다는 뜻

        # 2개의 세로단을 구성
        col = st.columns(2)

        with col[0]:
            st.download_button("csv 파일 다운로드",csv_data,file_name='exchange_rate_data.csv')

        with col[1]:
            st.download_button("엑셀 파일 다운로드",excel_data,file_name='exchange_rate_data.xlsx')

if __name__=="__main__":
    exchange_main()





    #pip list --format=freeze > requirements.txt   