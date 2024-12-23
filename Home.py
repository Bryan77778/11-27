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
    資料來自於政府資料開放平台、氣象資料開放平台、Windy，詳細資料如下
    1. 全台開放釣點位置
    2. 海域水質測站
    3. 海象數值模式預報資料-生活氣象-海水浴場、休閒漁港、海釣之波流模式預報資料
    4. 潮汐預報-未來1個月潮汐預報
    在此圖台可以查看釣魚點、水質測站的相對位置 \n
    同時也能在透過Windy了解即時氣象資料 \n
    並透過查詢潮汐及海像 \n
    與觀看及時影像 \n
    """
)


# 加入背景圖片
st.markdown(
    """
    <style>
    body {
        background-image: url('https://raw.githubusercontent.com/Bryan77778/11-27/main/%E8%83%8C%E6%99%AF%E5%9C%96%E7%89%87.png');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header("在左側選擇分頁")
