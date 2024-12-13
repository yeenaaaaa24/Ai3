#분류 결과 + 이미지 + 텍스트와 함께 분류 결과에 따라 다른 출력 보여주기
#파일 이름 streamlit_app.py
import streamlit as st
from fastai.vision.all import *
from PIL import Image
import gdown

# Google Drive 파일 ID
file_id = '1e-9_UjEFUKaybfkBS4A7egHhh3rvCodU'

# Google Drive에서 파일 다운로드 함수
@st.cache(allow_output_mutation=True)
def load_model_from_drive(file_id):
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'model.pkl'
    gdown.download(url, output, quiet=False)

    # Fastai 모델 로드
    learner = load_learner(output)
    return learner

def display_left_content(image, prediction, probs, labels):
    st.write("### 왼쪽: 기존 출력 결과")
    if image is not None:
        st.image(image, caption="업로드된 이미지", use_column_width=True)
    st.write(f"예측된 클래스: {prediction}")
    st.markdown("<h4>클래스별 확률:</h4>", unsafe_allow_html=True)
    for label, prob in zip(labels, probs):
        st.markdown(f"""
            <div style="background-color: #f0f0f0; border-radius: 5px; padding: 5px; margin: 5px 0;">
                <strong style="color: #333;">{label}:</strong>
                <div style="background-color: #d3d3d3; border-radius: 5px; width: 100%; padding: 2px;">
                    <div style="background-color: #4CAF50; width: {prob*100}%; padding: 5px 0; border-radius: 5px; text-align: center; color: white;">
                        {prob:.4f}
                    </div>
                </div>
        """, unsafe_allow_html=True)

def display_right_content(prediction, data):
    st.write("### 오른쪽: 동적 분류 결과")
    cols = st.columns(3)

    # 1st Row - Images
    for i in range(3):
        with cols[i]:
            st.image(data['images'][i], caption=f"이미지: {prediction}", use_column_width=True)
    # 2nd Row - YouTube Videos
    for i in range(3):
        with cols[i]:
            st.video(data['videos'][i])
            st.caption(f"유튜브: {prediction}")
    # 3rd Row - Text
    for i in range(3):
        with cols[i]:
            st.write(data['texts'][i])

# 모델 로드
st.write("모델을 로드 중입니다. 잠시만 기다려주세요...")
learner = load_model_from_drive(file_id)
st.success("모델이 성공적으로 로드되었습니다!")

labels = learner.dls.vocab

# 스타일링을 통해 페이지 마진 줄이기
st.markdown("""
    <style>
    .reportview-container .main .block-container {
        max-width: 90%;
        padding-top: 1rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 분류에 따라 다른 콘텐츠 관리
content_data = {
    labels[0]: {
        'images': [
            "https://img.mbn.co.kr/filewww/news/2021/04/29/1619694081608a9201190ab.jpg",
            "https://health.chosun.com/site/data/img_dir/2005/10/06/c2005100656029_01.jpg",
            "https://m.segye.com/content/image/2018/11/25/20181125786910.jpg"
        ],
        'videos': [
            "https://www.youtube.com/watch?v=wltwF4r4OBc",
            "https://www.youtube.com/watch?v=FLnZ2Tum20Y",
            "https://www.youtube.com/watch?v=OyBn7uinhGk"
        ],
        'texts': [
            "말단비대증 입니다.",
            "심각한 말단비대증 입니다.",
            "말단비대증으로 보보입니다."
        ]
    },
    labels[1]: {
        'images': [
            "https://img.hankyung.com/photo/202108/01.27299472.1.jpg",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-BSzFTK9i-nR87CRKDnrXMHEunWSTW_pyDw&s",
            "https://health.chosun.com/site/data/img_dir/2021/10/29/2021102901567_0.jpg"
        ],
        'videos': [
            "https://www.youtube.com/watch?v=p03auyh8s6Y",
            "https://www.youtube.com/watch?v=p03auyh8s6Y",
            "https://www.youtube.com/watch?v=-OnyIn26pKE"
        ],
        'texts': [
            "거인증 입니다",
            "심각한 거인증입니다",
            "거인증으로 보입니다다"
        ]
    },
    labels[2]: {
        'images': [
            "https://newsimg.hankookilbo.com/cms/articlerelease/2020/09/06/0b0c6eab-4b7e-413f-813a-23604a85a109.jpg",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRFLD5C0JzzHhat0D_ljFVf6GcA_gMQOAFSO6w0cY-WjIsX_mP8X6cPY61D6_Z59wb6TzU&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTMH_eJtB_GV7bfdU-7fG40YfA7orRV-UiVDg&s"
        ],
        'videos': [
            "https://www.youtube.com/watch?v=1ROwgiKrsB8",
            "https://www.youtube.com/watch?v=E4inX5Ri6D8",
            "https://www.youtube.com/watch?v=iZofSkQC9wc"
        ],
        'texts': [
            "다운증후군 입니다.",
            "심각한 다운증후군 입니다",
            "다운 증후군으로 보입니다   ],
       
        ]
    }
    
        

# 레이아웃 설정
left_column, right_column = st.columns([1, 2])  # 왼쪽과 오른쪽의 비율 조정

# 파일 업로드 컴포넌트 (jpg, png, jpeg, webp, tiff 지원)
uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "png", "jpeg", "webp", "tiff"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img = PILImage.create(uploaded_file)
    prediction, _, probs = learner.predict(img)

    with left_column:
        display_left_content(image, prediction, probs, labels)

    with right_column:
        # 분류 결과에 따른 콘텐츠 선택
        data = content_data.get(prediction, {
            'images': ["https://via.placeholder.com/300"] * 3,
            'videos': ["https://www.youtube.com/watch?v=3JZ_D3ELwOQ"] * 3,
            'texts': ["기본 텍스트"] * 3
        })
        display_right_content(prediction, data)

