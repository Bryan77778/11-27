import streamlit as st
import leafmap.foliumap as leafmap

# GeoJSON 資料 URL
water_quality_stations_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E5%9F%9F%E6%B0%B4%E8%B3%AA%E6%B8%AC%E7%AB%99.geojson"
fishing_spots_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E5%85%A8%E5%8F%B0%E9%96%8B%E6%94%BE%E9%87%A3%E9%BB%9E%E4%BD%8D%E7%BD%AE%20(1).geojson"

# Streamlit 應用標題
st.title("Windy API 與水質測站點位地圖 Viewer")

# 提供底圖選項
basemap_options = list(leafmap.basemaps.keys())

# 第一行地圖顯示
st.write("### 第一行地圖")
row1_col1, row1_col2 = st.columns(2)

# 左側地圖 - 顯示水質測站
with row1_col1:
    st.write("#### 左側地圖：水質測站點位")
    basemap1 = st.selectbox("選擇左側地圖的底圖:", basemap_options, index=basemap_options.index("OpenStreetMap"))
    
    # 創建 Leafmap 地圖
    m1 = leafmap.Map(center=[23.5, 121], zoom=7)
    m1.add_basemap(basemap1)
    m1.add_geojson(water_quality_stations_url, layer_name="Water Quality Stations")
    m1.to_streamlit(height=500)

# 右側地圖 - 整合 Windy API + 水質測站
with row1_col2:
    st.write("#### 右側地圖：Windy 風場圖與水質測站點位")
    
    # 創建 Leafmap 地圖
    m2 = leafmap.Map(center=[23.5, 121], zoom=7)
    
    # 加入 Windy 風場瓦片圖層
    windy_tile_layer = "https://tiles.windy.com/tiles/v10.0/dark/256/{z}/{x}/{y}.png"
    m2.add_tile_layer(
        windy_tile_layer,
        name="Windy Wind Layer",
        attribution="© Windy.com"
    )
    
    # 加入水質測站點位 (GeoJSON)
    m2.add_geojson(water_quality_stations_url, layer_name="Water Quality Stations")
    
    # 顯示地圖
    m2.to_streamlit(height=500)
