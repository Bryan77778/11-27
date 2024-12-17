import streamlit as st
import leafmap.foliumap as leafmap

# 設定頁面配置
st.set_page_config(layout="wide")

# GeoJSON 資料 URL
water_quality_stations_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E5%9F%9F%E6%B0%B4%E8%B3%AA%E6%B8%AC%E7%AB%99.geojson"

# Streamlit 應用標題
st.title("分割地圖展示：風速底圖與水質測站點位")

# 說明與側邊欄
markdown = """
本範例展示了如何使用 Split Map 功能同時呈現不同圖層。  
- **左側**：模擬風速底圖  
- **右側**：水質測站點位  
"""
st.sidebar.title("說明")
st.sidebar.info(markdown)

# 創建分割地圖
m = leafmap.Map(center=[23.5, 121], zoom=7)

# Split Map 功能：左側與右側地圖
m.split_map(
    left_layer="CartoDB Dark Matter",  # 左側底圖（類似風速的暗色底圖）
    right_layer="OpenStreetMap"        # 右側底圖
)

# 加入水質測站的 GeoJSON 點位（右側圖層）
m.add_geojson(water_quality_stations_url, layer_name="水質測站點位")

# 加入圖例與標題
m.add_legend(title="圖層說明", legend_dict={"Water Quality Stations": "blue"})

# 顯示地圖
m.to_streamlit(height=700)

    m.add_geojson(water_quality_stations_url, layer_name="水質測站點位")
    m.to_streamlit(height=500)

