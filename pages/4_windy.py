import streamlit as st
import leafmap.foliumap as leafmap

# GeoJSON 資料 URL
water_quality_stations_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E5%9F%9F%E6%B0%B4%E8%B3%AA%E6%B8%AC%E7%AB%99.geojson"

# Streamlit 應用標題
st.title("分割地圖展示：Windy 風速與水質測站點位")

# 第一行地圖顯示
st.write("### 第一行地圖")
row1_col1, row1_col2 = st.columns(2)

# 左側地圖 - Windy 動態風速圖 (iframe)
with row1_col1:
    st.write("#### 左側地圖：Windy 動態風速")
    windy_embed_code = """
    <iframe 
        width="100%" 
        height="500" 
        src="https://embed.windy.com/embed2.html?lat=23.5&lon=121&zoom=6&level=surface&overlay=wind&menu=&message=&marker=&calendar=&pressure=&type=map&location=coordinates&detail=&detailLat=23.5&detailLon=121&metricWind=default&metricTemp=default&radarRange=-1" 
        frameborder="0">
    </iframe>
    """
    st.components.v1.html(windy_embed_code, height=500)

# 右側地圖 - 水質測站點位
with row1_col2:
    st.write("#### 右側地圖：水質測站點位")
    # 創建 Leafmap 地圖
    m = leafmap.Map(center=[23.5, 121], zoom=7)
    m.add_basemap("OpenStreetMap")
    m.add_geojson(water_quality_stations_url, layer_name="水質測站點位")
    m.to_streamlit(height=500)

