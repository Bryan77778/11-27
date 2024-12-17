import streamlit as st
import leafmap.foliumap as leafmap
from streamlit_folium import st_folium

# 固定 Windy API Key
WINDY_API_KEY = "Q2V4GyCCzdkfMxBXqrplP2UbxXLjBrEn"

# GeoJSON 資料 URL
water_quality_stations_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E5%9F%9F%E6%B0%B4%E8%B3%AA%E6%B8%AC%E7%AB%99.geojson"

# Streamlit 應用標題
st.title("互動地圖展示：點擊水質測站以更新 Windy 圖台")

# 1. 設定地圖的初始中心位置
initial_lat, initial_lon = 23.5, 121  # 台灣中間位置
zoom_level = 6

# 2. 左側 Windy 動態風速圖
st.write("### 左側：Windy 動態風速")
if "windy_lat" not in st.session_state:
    st.session_state["windy_lat"] = initial_lat
    st.session_state["windy_lon"] = initial_lon

windy_url = f"""
<iframe 
    width="100%" 
    height="500" 
    src="https://embed.windy.com/embed2.html?lat={st.session_state['windy_lat']}&lon={st.session_state['windy_lon']}&zoom=8&level=surface&overlay=wind&menu=&message=&marker=&calendar=&pressure=&type=map&location=coordinates&detail=&detailLat={st.session_state['windy_lat']}&detailLon={st.session_state['windy_lon']}&metricWind=default&metricTemp=default&radarRange=-1&key={WINDY_API_KEY}" 
    frameborder="0">
</iframe>
"""
st.components.v1.html(windy_url, height=500)

# 3. 右側水質測站點位地圖（可點擊互動）
st.write("### 右側：水質測站點位")

# 創建 Leafmap 地圖
m = leafmap.Map(center=[initial_lat, initial_lon], zoom=zoom_level)
m.add_basemap("OpenStreetMap")
m.add_geojson(water_quality_stations_url, layer_name="水質測站點位")

# 加入點擊事件
click_info = st_folium(m, width=700, height=500)

# 4. 偵測點擊事件並更新 Windy iframe
if click_info and click_info["last_clicked"]:
    clicked_lat = click_info["last_clicked"]["lat"]
    clicked_lon = click_info["last_clicked"]["lng"]
    st.session_state["windy_lat"] = clicked_lat
    st.session_state["windy_lon"] = clicked_lon
    st.experimental_rerun()

    m.add_geojson(water_quality_stations_url, layer_name="水質測站點位")
    m.to_streamlit(height=500)
