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
    {"name": "台江國家公園-北汕尾水鳥保護區", "coords": [23.020093, 120.142991], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "台江國家公園-北汕尾水鳥保護區", "coords": [23.020093, 120.142991], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "台江國家公園-北汕尾水鳥保護區", "coords": [23.020093, 120.142991], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "台江國家公園-北汕尾水鳥保護區", "coords": [23.020093, 120.142991], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "台江國家公園-北汕尾水鳥保護區", "coords": [23.020093, 120.142991], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "台江國家公園-北汕尾水鳥保護區", "coords": [23.020093, 120.142991], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "台江國家公園-北汕尾水鳥保護區", "coords": [23.020093, 120.142991], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "台江國家公園-北汕尾水鳥保護區", "coords": [23.020093, 120.142991], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "台江國家公園-北汕尾水鳥保護區", "coords": [23.020093, 120.142991], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "台江國家公園-北汕尾水鳥保護區", "coords": [23.020093, 120.142991], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "台江國家公園-北汕尾水鳥保護區", "coords": [23.020093, 120.142991], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "台江國家公園-北汕尾水鳥保護區", "coords": [23.020093, 120.142991], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "台江國家公園-北汕尾水鳥保護區", "coords": [23.020093, 120.142991], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "台江國家公園-北汕尾水鳥保護區", "coords": [23.020093, 120.142991], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},
    {"name": "台江國家公園-北汕尾水鳥保護區", "coords": [23.020093, 120.142991], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"},]

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
