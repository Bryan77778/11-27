import streamlit as st
import leafmap.foliumap as leafmap
from streamlit_folium import st_folium

# 固定 Windy API Key
WINDY_API_KEY = "Q2V4GyCCzdkfMxBXqrplP2UbxXLjBrEn"

# GeoJSON 資料 URL
water_quality_stations_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E5%9F%9F%E6%B0%B4%E8%B3%AA%E6%B8%AC%E7%AB%99.geojson"

# Streamlit 應用標題
st.title("並排互動地圖：點擊水質測站以更新 Windy 圖台")

# 設定地圖的初始中心位置與縮放級別
initial_lat, initial_lon = 23.5, 121  # 台灣中間位置
zoom_level = 6

# 初始化 session_state
if "windy_lat" not in st.session_state:
    st.session_state["windy_lat"] = initial_lat
    st.session_state["windy_lon"] = initial_lon
    st.session_state["windy_zoom"] = zoom_level

# 建立左右分欄
col1, col2 = st.columns(2)

# 左側：Windy 動態風速圖
with col1:
    st.write("### 左側：Windy 動態風速")
    windy_url = f"""
    <iframe 
        width="100%" 
        height="500" 
        src="https://embed.windy.com/embed2.html?lat={st.session_state['windy_lat']}&lon={st.session_state['windy_lon']}&zoom={st.session_state['windy_zoom']}&level=surface&overlay=wind&menu=&message=&marker=&calendar=&pressure=&type=map&location=coordinates&detail=&detailLat={st.session_state['windy_lat']}&detailLon={st.session_state['windy_lon']}&metricWind=default&metricTemp=default&radarRange=-1&key={WINDY_API_KEY}" 
        frameborder="0">
    </iframe>
    """
    st.components.v1.html(windy_url, height=500)

# 右側：水質測站點位地圖
with col2:
    st.write("### 右側：水質測站點位")
    m = leafmap.Map(center=[st.session_state["windy_lat"], st.session_state["windy_lon"]], zoom=zoom_level)
    m.add_basemap("OpenStreetMap")
    m.add_geojson(water_quality_stations_url, layer_name="水質測站點位")

    # 處理點擊事件
    click_info = st_folium(m, width=700, height=500)

# 偵測點擊並更新 Windy iframe
if click_info and click_info.get("last_clicked"):
    clicked_lat = click_info["last_clicked"]["lat"]
    clicked_lon = click_info["last_clicked"]["lng"]
    st.session_state["windy_lat"] = clicked_lat
    st.session_state["windy_lon"] = clicked_lon
    st.session_state["windy_zoom"] = 12  # 放大至適合級別
    st.rerun()

