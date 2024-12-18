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
    {"name": "台江國家公園", "coords": [23.0024, 120.1399], "youtube_url": "https://www.youtube.com/watch?v=FES0gWTFUHQ&list=PLDm4hXBol5DE9QmiOdgyzYmS2jRzenhUv&index=8"}
]

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
