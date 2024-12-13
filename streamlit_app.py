#기본적인 Streamlit 페이지 예제

# streamlit_app.py
import streamlit as st
import pandas as pd

# 1. 제목
st.title("손예나의 스트림릿 서비스")

# 2. 부제목
st.subheader("와 멋진 서비스")

# 3. 판다스 데이터프레임 기반 표 출력
df = pd.DataFrame({
    "이름": ["손예나", "손예소", "이종원"],
    "나이;": [18, 30, 29],
    "나": ["Korea", "USA", "UK"]
})
st.write("데이터프레임 예제")
st.dataframe(df)

# 4. HTML 활용 예제
st.write("HTML 예제")
st.markdown(
    """
    <div style="color: blue; font-size: 20px;">
        HTML을 활용한 예시 텍스트입니다.
    </div>
    """,
    unsafe_allow_html=True
)

# 5. HTML과 CSS 활용 예제
st.write("HTML과 CSS 예제")
st.markdown(
    """
    <style>
    .styled-box {
        padding: 10px;
        margin: 5px;
        background-color: lightgreen;
        border-radius: 5px;
        color: darkgreen;
    }
    </style>
    <div class="styled-box">
        HTML과 CSS를 함께 사용하여 스타일링한 박스입니다.
    </div>
    """,
    unsafe_allow_html=True
)

# 6. 이미지 표시
st.write("이미지 표시 예제")
st.image("https://img.wkorea.com/w/2022/10/style_634f9b4c8c907-500x354-1666161931.jpg", caption="Streamlit 로고")

# 7. 유튜브 링크 (썸네일 표시)
st.write("유튜브 동영상 예제")
st.video("https://www.youtube.com/watch?v=QnCT0Au68oE")

