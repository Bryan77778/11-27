# 完整 Streamlit 應用程式
import streamlit as st
import leafmap.foliumap as leafmap

# 設定 Streamlit 網頁標題與描述
st.set_page_config(page_title="地圖上的 YouTube 連結", layout="wide")
st.title("地圖上的 YouTube 連結")
st.markdown("""
此應用展示如何在地圖上添加帶有 YouTube 連結的點座標。
- 點擊地圖上的點標記以查看詳細資訊。
- 點擊彈出窗口中的連結以打開 YouTube。
""")

# 定義多個點的數據
points = [
    {"name": "台江國家公園-北汕尾水鳥保護區", "coords": [23.020093, 120.142991], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "台江國家公園-六孔碼頭", "coords": [23.123639, 120.078626], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "新北野柳", "coords": [25.209065, 121.693489], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "雲林萡子寮", "coords": [23.629572, 120.140660], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "宜蘭大里", "coords": [24.965018, 121.922791], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "高雄西子灣", "coords": [22.622998, 120.261220], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "基隆碧砂漁港", "coords": [25.145441, 121.789814], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "宜蘭蘇澳港", "coords": [24.574382, 121.869418], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "臺東富岡漁港", "coords": [22.791453, 121.192707], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "新北市沙崙", "coords": [25.189082, 121.413410], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "新北福隆", "coords": [25.026916, 121.938796], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "台南安平港", "coords": [22.991701, 120.154315], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "小琉球杉福港", "coords": [22.341942, 120.362633], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "小琉球漁福漁港", "coords": [22.347307, 120.388527], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "台東金樽漁港", "coords": [22.955882, 121.295237], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "台東富山漁港", "coords": [22.821392, 121.191813], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "台東杉原灣", "coords": [22.830737, 121.186151], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "台中高美濕地", "coords": [24.312216, 120.549776], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "花蓮七星潭", "coords": [24.027598, 121.631614], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "台東三仙台", "coords": [23.124095, 121.409902], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "桃園永安漁港", "coords": [24.990360, 121.011923], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "高雄蚵寮國小海岸", "coords": [22.732847, 120.247749], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "花蓮海岸忘憂亭", "coords": [23.969596, 121.612821], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "宜蘭外澳沙灘 ", "coords": [24.877786, 121.843179], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "綠島柴口", "coords": [22.677401, 121.482408], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "東引遊客中心外平台", "coords": [26.364045, 120.483597], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "南竿鐵堡", "coords": [26.141958, 119.920947], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "花蓮南濱", "coords": [23.961864, 121.607661], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "嘉義布袋港", "coords": [23.378488, 120.138065], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "新北萬里港", "coords": [25.181092, 121.697284], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "屏東後壁湖", "coords": [21.944897, 120.744585], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "屏東合界海岸", "coords": [21.955620, 120.712336], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "宜蘭石城漁港", "coords": [24.979793, 121.950841], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "新北中角海濱", "coords": [25.241362, 121.633588], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "基隆潮境海灣", "coords": [25.143973, 121.803787], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "基隆外木山漁港", "coords": [25.159178, 121.734041], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "屏東佳樂水", "coords": [21.994685, 120.865195], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "屏東海生館", "coords": [22.045920, 120.695635], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "宜蘭蘇澳無尾港", "coords": [24.615391, 121.859491], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "新北龍洞", "coords": [25.111316, 121.922937], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "新北鼻頭港", "coords": [25.124196, 121.912837], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "台南觀夕平台", "coords": [22.989880, 120.146303], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "澎湖觀音亭海灣", "coords": [23.567821, 119.561160], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "新北風箏坪", "coords": [25.207170, 121.662895], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "澎湖青灣", "coords": [23.527215, 119.557186], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"}]

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

# 顯示數據表格
st.markdown("### 點座標與 YouTube 連結")
st.dataframe(points)
