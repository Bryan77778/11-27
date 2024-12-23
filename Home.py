import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
Web App URL: <https://geotemplate.streamlit.app>
GitHub Repository: <https://github.com/giswqs/streamlit-multipage-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

# Customize page title
st.title("釣魚地點互動式圖台")

st.markdown(
    """
    <style>
    .stMarkdown {
        font-size: 20px;  /* 設定字體大小 */
        color: white;  /* 設定字體顏色為白色 */
    }
    </style>
    <div class="stMarkdown">
    資料來自於政府資料開放平台、氣象資料開放平台、Windy，詳細資料如下 \n
    1. 全台開放釣點位置 \n
    2. 海域水質測站 \n
    3. 海象數值模式預報資料-生活氣象-海水浴場、休閒漁港、海釣之波流模式預報資料 \n
    4. 潮汐預報-未來1個月潮汐預報 \n
    在此圖台可以查看釣魚點、水質測站的相對位置 \n
    同時也能在透過Windy了解即時氣象資料 \n
    並透過查詢潮汐及海像 \n
    與觀看及時影像 \n
    </div>
    """,
    unsafe_allow_html=True
)
st.header("在左側選擇分頁")

st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://i.imgur.com/D6zbNRN.png'); 
        background-size: cover;  /* 讓背景圖像填滿整個視窗 */
        background-position: center;  /* 背景圖像居中 */
        color: white;  /* 設定字體顏色為白色 */
    }
     /* 調整背景圖片的透明度 */
    .stApp::after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url('https://i.imgur.com/D6zbNRN.png');
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
        opacity: 0.5;  /* 調整透明度，0表示完全透明，1表示完全不透明 */
        z-index: -1;  /* 讓背景圖片在內容下面 */
    }
    </style>
    """,
    unsafe_allow_html=True
)
