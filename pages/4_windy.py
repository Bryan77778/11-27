pip install streamlit-folium
import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import json

# Streamlit 應用標題
st.title("Windy API 與水質測站地圖 Viewer")

# 固定 Windy API Key 和其他設定
api_key = "Q2V4GyCCzdkfMxBXqrplP2UbxXLjBrEn"
water_quality_stations_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E5%9F%9F%E6%B0%B4%E8%B3%AA%E6%B8%AC%E7%AB%99.geojson"

# 地圖初始設定
st.write("以下地圖顯示 Windy 天氣預報與水質測站的位置：")

# 創建 Folium 地圖
m = folium.Map(location=[23.5, 121], zoom_start=7)

# 嵌入 Windy API iframe
windy_embed_code = f"""
<iframe 
    width="800" 
    height="600" 
    src="https://embed.windy.com/embed2.html?lat=23.5&lon=121&zoom=6&level=surface&overlay=wind&menu=&message=&marker=&calendar=&pressure=&type=map&location=coordinates&detail=&detailLat=23.5&detailLon=121&metricWind=default&metricTemp=default&radarRange=-1&key={api_key}" 
    frameborder="0">
</iframe>
"""
st.components.v1.html(windy_embed_code, height=600)

# 讀取水質測站資料
try:
    response = requests.get(water_quality_stations_url)
    if response.status_code == 200:
        geojson_data = response.json()
        # 在地圖上加入水質測站
        folium.GeoJson(
            geojson_data,
            name="水質測站",
            tooltip=folium.GeoJsonTooltip(fields=["name"], aliases=["測站名稱:"])
        ).add_to(m)
        # 顯示 Folium 地圖
        st_folium(m, width=800, height=600)
    else:
        st.error("無法讀取水質測站資料，請檢查網址。")
except Exception as e:
    st.error(f"發生錯誤: {e}")
