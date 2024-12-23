# 完整 Streamlit 應用程式
import streamlit as st
import leafmap.foliumap as leafmap

# 設定 Streamlit 網頁標題與描述
st.set_page_config(page_title="地圖上的 YouTube 連結", layout="wide")
st.title("地圖上的 YouTube 連結")
st.markdown(
    """
    <style>
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
                          url('https://i.imgur.com/D6zbNRN.png'); /* 添加半透明黑色遮罩 */
        background-size: cover; /* 背景圖片填滿窗口 */
        background-position: center; /* 背景圖片居中 */
        color: white; /* 全局字體顏色設置為白色 */
    }
    .custom-text {
        font-size: 18px; /* 設置文字大小 */
        line-height: 1.6; /* 行距 */
        color: white; /* 設置文字顏色 */
    }
    .stSelectbox div[role="combobox"] {
        color: white;  /* 下拉選單內的文字設置為黑色（避免與白色背景衝突） */
        background-color: white;  /* 下拉選單背景設置為白色 */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="custom-text">
    此應用展示如何在地圖上添加帶有 YouTube 連結的點座標。/n
    - 點擊地圖上的點標記以查看詳細資訊。 /n
    - 點擊彈出窗口中的連結以打開 YouTube。 /n
    </div>
    """,
    unsafe_allow_html=True
)


# 定義多個點的數據
points = [
    {"name": "台江國家公園-北汕尾水鳥保護區", "coords": [23.020093, 120.142991], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "台江國家公園-六孔碼頭", "coords": [23.123639, 120.078626], "youtube_url": "https://www.youtube.com/watch?v=oNL7o865EiY&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=9"},
    {"name": "新北野柳", "coords": [25.209065, 121.693489], "youtube_url": "https://www.youtube.com/watch?v=KKjp-ToFSbQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=11"},
    {"name": "雲林萡子寮", "coords": [23.629572, 120.140660], "youtube_url": "https://www.youtube.com/watch?v=HaigwEFfgyQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=36"},
    {"name": "宜蘭大里", "coords": [24.965018, 121.922791], "youtube_url": "https://www.youtube.com/watch?v=68qSYgEjl4k&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=44"},
    {"name": "高雄西子灣", "coords": [22.622998, 120.261220], "youtube_url": "https://www.youtube.com/watch?v=Jsz-d62r-Eg&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=38"},
    {"name": "基隆碧砂漁港", "coords": [25.145441, 121.789814], "youtube_url": "https://www.youtube.com/watch?v=VdR7tXWE7vM&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=42"},
    {"name": "宜蘭蘇澳港", "coords": [24.574382, 121.869418], "youtube_url": "https://www.youtube.com/watch?v=3Q1kPyfX638&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=40"},
    {"name": "臺東富岡漁港", "coords": [22.791453, 121.192707], "youtube_url": "https://www.youtube.com/watch?v=VG8ASWpuUvE&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=43"},
    {"name": "新北市沙崙", "coords": [25.189082, 121.413410], "youtube_url": "https://www.youtube.com/watch?v=VG8ASWpuUvE&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=43"},
    {"name": "新北福隆", "coords": [25.026916, 121.938796], "youtube_url": "https://www.youtube.com/watch?v=YF72-Fi5Rkc&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=47"},
    {"name": "台南安平港", "coords": [22.991701, 120.154315], "youtube_url": "https://www.youtube.com/watch?v=_fwtmj0nxGQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=48"},
    {"name": "小琉球杉福港", "coords": [22.341942, 120.362633], "youtube_url": "https://www.youtube.com/watch?v=wVVFQzTvWWs&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=90"},
    {"name": "小琉球漁福漁港", "coords": [22.347307, 120.388527], "youtube_url": "https://www.youtube.com/watch?v=FPJX8g9RUds&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=96"},
    {"name": "台東金樽漁港", "coords": [22.955882, 121.295237], "youtube_url": "https://www.youtube.com/watch?v=q3KJt-SZc2s&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=117"},
    {"name": "台東富山漁港", "coords": [22.821392, 121.191813], "youtube_url": "https://www.youtube.com/watch?v=Rsq95SQ26bY&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=119"},
    {"name": "台東杉原灣", "coords": [22.830737, 121.186151], "youtube_url": "https://www.youtube.com/watch?v=VqS_Y8ZCj6M&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=120"},
    {"name": "台中高美濕地", "coords": [24.312216, 120.549776], "youtube_url": "https://www.youtube.com/watch?v=fjhg3gAnMFg&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=122"},
    {"name": "花蓮七星潭", "coords": [24.027598, 121.631614], "youtube_url": "https://www.youtube.com/watch?v=j3l32VFi5M8&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=125"},
    {"name": "台東三仙台", "coords": [23.124095, 121.409902], "youtube_url": "https://www.youtube.com/watch?v=dQ7Sd6PGLdA&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=133"},
    {"name": "桃園永安漁港", "coords": [24.990360, 121.011923], "youtube_url": "https://www.youtube.com/watch?v=tD_a03trUvE&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=134"},
    {"name": "高雄蚵寮國小海岸", "coords": [22.732847, 120.247749], "youtube_url": "https://www.youtube.com/watch?v=sKrqs-5Auqo&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=152"},
    {"name": "花蓮海岸忘憂亭", "coords": [23.969596, 121.612821], "youtube_url": "https://www.youtube.com/watch?v=Ic6hqus0tjA&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=155"},
    {"name": "宜蘭外澳沙灘 ", "coords": [24.877786, 121.843179], "youtube_url": "https://www.youtube.com/watch?v=UgoT-QTbYvo&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=162"},
    {"name": "綠島柴口", "coords": [22.677401, 121.482408], "youtube_url": "https://www.youtube.com/watch?v=zQQSfAkjCJc&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=176"},
    {"name": "東引遊客中心外平台", "coords": [26.364045, 120.483597], "youtube_url": "https://www.youtube.com/watch?v=5Hc_6uiokds&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=177"},
    {"name": "南竿鐵堡", "coords": [26.141958, 119.920947], "youtube_url": "https://www.youtube.com/watch?v=NVf3j-5I1Fk&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=179"},
    {"name": "花蓮南濱", "coords": [23.961864, 121.607661], "youtube_url": "https://www.youtube.com/watch?v=OQnwVN5lzsk&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=188"},
    {"name": "嘉義布袋港", "coords": [23.378488, 120.138065], "youtube_url": "https://www.youtube.com/watch?v=TCfXAzeeGik&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=212"},
    {"name": "新北萬里港", "coords": [25.181092, 121.697284], "youtube_url": "https://www.youtube.com/watch?v=Shp8KdJK9-Y&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=214"},
    {"name": "屏東後壁湖", "coords": [21.944897, 120.744585], "youtube_url": "https://www.youtube.com/watch?v=yDxCT1q9CrE&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=215"},
    {"name": "屏東合界海岸", "coords": [21.955620, 120.712336], "youtube_url": "https://www.youtube.com/watch?v=TtRGpQGrkqo&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=217"},
    {"name": "宜蘭石城漁港", "coords": [24.979793, 121.950841], "youtube_url": "https://www.youtube.com/watch?v=X76Dkt_fPG0&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=219"},
    {"name": "新北中角海濱", "coords": [25.241362, 121.633588], "youtube_url": "https://www.youtube.com/watch?v=5FCHZP2GMog&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=221"},
    {"name": "基隆潮境海灣", "coords": [25.143973, 121.803787], "youtube_url": "https://www.youtube.com/watch?v=jzAxB157yb8&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=222"},
    {"name": "基隆外木山漁港", "coords": [25.159178, 121.734041], "youtube_url": "https://www.youtube.com/watch?v=LInNQYAbAwQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=224"},
    {"name": "屏東佳樂水", "coords": [21.994685, 120.865195], "youtube_url": "https://www.youtube.com/watch?v=KBz0yn-F_SY&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=225"},
    {"name": "屏東海生館", "coords": [22.045920, 120.695635], "youtube_url": "https://www.youtube.com/watch?v=L0NX2-8_J48&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=227"},
    {"name": "宜蘭蘇澳無尾港", "coords": [24.615391, 121.859491], "youtube_url": "https://www.youtube.com/watch?v=gPeJuFuNcRc&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=228"},
    {"name": "新北龍洞", "coords": [25.111316, 121.922937], "youtube_url": "https://www.youtube.com/watch?v=p4Pa4iFpzR8&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=238"},
    {"name": "新北鼻頭港", "coords": [25.124196, 121.912837], "youtube_url": "https://www.youtube.com/watch?v=EpbjwNdOxT8&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=250"},
    {"name": "台南觀夕平台", "coords": [22.989880, 120.146303], "youtube_url": "https://www.youtube.com/watch?v=nblKKkuuDsk&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=356"},
    {"name": "澎湖觀音亭海灣", "coords": [23.567821, 119.561160], "youtube_url": "https://www.youtube.com/watch?v=xGilwi36tcc&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=351"},
    {"name": "新北風箏坪", "coords": [25.207170, 121.662895], "youtube_url": "https://www.youtube.com/watch?v=Dty_37LrDck&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=349"},
    {"name": "澎湖青灣", "coords": [23.527215, 119.557186], "youtube_url": "https://www.youtube.com/watch?v=ewdX46NzMWo&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=346"}]

# 創建地圖
m = leafmap.Map(center=(23.5, 120.5), zoom=10)

# 添加點標記到地圖
for point in points:
    popup_html = f"""
    <h4>{point['name']}</h4>
    <a href="{point['youtube_url']}" target="_blank">觀看 YouTube</a>
    """
    m.add_marker(location=point["coords"], popup=popup_html)

# 使用 Streamlit 顯示地圖
st.markdown("### 地圖")
m.to_streamlit(height=600)

# 顯示數據表格
st.markdown("### 點座標與 YouTube 連結")
st.dataframe(points)

