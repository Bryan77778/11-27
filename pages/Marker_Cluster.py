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

col1, col2 = st.columns([1, 1])



# 在左側顯示地圖
with col1:
    options = list(leafmap.basemaps.keys())
    basemap = st.selectbox("【水質測站】選擇第一張地圖底圖:", options, index=options.index("OpenTopoMap"))

    water_quality_stations_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E5%9F%9F%E6%B0%B4%E8%B3%AA%E6%B8%AC%E7%AB%99.geojson"
    fishing_spots_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E5%85%A8%E5%8F%B0%E9%96%8B%E6%94%BE%E9%87%A3%E9%BB%9E%E4%BD%8D%E7%BD%AE%20(1).geojson"

    m1 = leafmap.Map(center=[25, 121], zoom=7)
    m1.add_basemap(basemap, name="水質測站")
    
    # 讀取並顯示水質監測站資料
    water_quality_stations_gdf = gpd.read_file(water_quality_stations_url)
    m1.add_points_from_xy(
        water_quality_stations_gdf,
        x="LON",  # 根據實際資料調整欄位名稱
        y="LAT",  # 根據實際資料調整欄位名稱
        spin=True,
        add_legend=True,
        layer_name="水質監測站"
    )
    m1.to_streamlit(height=700)

# 第二個地圖（顯示釣魚點）
with col2:
    basemap = st.selectbox("【垂釣地點】選擇第二張地圖底圖:", options, index=options.index("OpenStreetMap"))
    
    m2 = leafmap.Map(center=[25, 121], zoom=7)
    m2.add_basemap(basemap, name="垂釣地點")
    
    # 讀取並顯示釣魚點資料
    fishing_spots_gdf = gpd.read_file(fishing_spots_url)
    m2.add_points_from_xy(
        fishing_spots_gdf,
        x="XPOS",  # 根據實際資料調整欄位名稱
        y="YPOS",  # 根據實際資料調整欄位名稱
        spin=True,
        add_legend=True,
        layer_name="釣魚點"
    )
    m2.to_streamlit(height=700)

