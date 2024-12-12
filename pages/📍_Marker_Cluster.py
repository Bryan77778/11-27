import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

st.set_page_config(layout="wide")

markdown = """
Web App URL: <https://geotemplate.streamlit.app>
GitHub Repository: <https://github.com/giswqs/streamlit-multipage-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("Marker Cluster")

col1, col2 = st.columns([3, 1])

with col2:
    options = list(leafmap.basemaps.keys())
    basemap = st.selectbox("選擇底圖:", options, index=options.index("OpenTopoMap"))

# 在左側顯示地圖
with col1:
    m = leafmap.Map(
        center=[40, -100], zoom=4, 
        locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
    )
    m.add_basemap(basemap)

    # 定義 GeoJSON 資料的 URL
    water_quality_stations_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E5%9F%9F%E6%B0%B4%E8%B3%AA%E6%B8%AC%E7%AB%99.geojson"
    fishing_spots_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E5%85%A8%E5%8F%B0%E9%96%8B%E6%94%BE%E9%87%A3%E9%BB%9E%E4%BD%8D%E7%BD%AE%20(1).geojson"
    
    # 添加水質監測站資料
    water_quality_stations_gdf = gpd.read_file(water_quality_stations_url)
    m.add_points_from_xy(
        water_quality_stations_gdf,
        x="lon",  # 根據實際資料調整欄位名稱
        y="lat",  # 根據實際資料調整欄位名稱
        spin=True,
        add_legend=True,
        layer_name="水質監測站"
    )
    
    # 添加釣魚點資料
    fishing_spots_gdf = gpd.read_file(fishing_spots_url)
    m.add_points_from_xy(
        fishing_spots_gdf,
        x="lon",  # 根據實際資料調整欄位名稱
        y="lat",  # 根據實際資料調整欄位名稱
        spin=True,
        add_legend=True,
        layer_name="釣魚點"
    )

    # 顯示地圖
    m.to_streamlit(height=700)
