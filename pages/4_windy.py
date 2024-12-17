import streamlit as st
import leafmap.foliumap as leafmap
from streamlit_folium import st_folium

# 固定 Windy API Key
WINDY_API_KEY = "Q2V4GyCCzdkfMxBXqrplP2UbxXLjBrEn"

# GeoJSON 資料 URL
water_quality_stations_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E5%9F%9F%E6%B0%B4%E8%B3%AA%E6%B8%AC%E7%AB%99.geojson"

# Streamlit 應用標題
st.title("互動地圖展示：點擊水質測站以更新 Windy 圖台")

# 1. 初始化 Windy 地圖中心點位置
if "windy_lat" not in st.session_state:
    st.session_state["windy_lat"] = 23.5  # 初始緯度
if "windy_lon" not in st.session_state:
    st.session_state["windy_lon"] = 121   # 初始經度
if "windy_zoom" not in st.session_state:
    st.session_state["windy_zoom"] = 10   # 初始縮放級別

# 2. 使用 Columns 進行左右分割顯示
col1, col2 = st.columns(2)

# 3. 左側 Windy 動態風速圖 (放大後的 zoom 值)
with col1:
    st.write("#### 左側地圖：Windy 動態風速 (點擊後放大)")
    windy_url = f"""
    <iframe 
        width="100%" 
        height="500" 
        src="https://embed.windy.com/embed2.html?lat={st.session_state['windy_lat']}&lon={st.session_state['windy_lon']}&zoom={st.session_state['windy_zoom']}&level=surface&overlay=wind&menu=&message=&marker=&calendar=&pressure=&type=map&location=coordinates&detail=&detailLat={st.session_state['windy_lat']}&detailLon={st.session_state['windy_lon']}&metricWind=default&metricTemp=default&radarRange=-1&key={WINDY_API_KEY}" 
        frameborder="0">
    </iframe>
    """
    st.components.v1.html(windy_url, height=500)

# 4. 右側地圖：水質測站點位 (互動)
with col2:
    st.write("#### 右側地圖：水質測站點位")
    m = leafmap.Map(center=[st.session_state["windy_lat"], st.session_state["windy_lon"]], zoom=7)
    m.add_basemap("OpenStreetMap")
    m.add_geojson(water_quality_stations_url, layer_name="水質測站點位")

    # 透過 st_folium 取得點擊資訊
    click_info = st_folium(m, width=700, height=500)

# 5. 更新 Windy 圖台位置與放大級別
if click_info and click_info["last_clicked"]:
    st.session_state["windy_lat"] = click_info["last_clicked"]["lat"]
    st.session_state["windy_lon"] = click_info["last_clicked"]["lng"]
    st.session_state["windy_zoom"] = 12  # 點擊後放大至更高的級別
    st.experimental_rerun()

