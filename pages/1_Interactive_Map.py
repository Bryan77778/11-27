import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

# 左側欄的資訊
markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

# 主頁標題
st.title("Interactive Map")

# 分成兩個區塊 (地圖與選擇欄)
col1, col2 = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("OpenTopoMap")

with col2:
    basemap = st.selectbox("Select a basemap:", options, index)

# GeoJSON URL
water_quality_stations_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E5%9F%9F%E6%B0%B4%E8%B3%AA%E6%B8%AC%E7%AB%99.geojson"
fishing_spots_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E5%85%A8%E5%8F%B0%E9%96%8B%E6%94%BE%E9%87%A3%E9%BB%9E%E4%BD%8D%E7%BD%AE%20(1).geojson"

# 使用 GeoPandas 讀取資料
try:
    water_quality_stations_gdf = gpd.read_file(water_quality_stations_url)
    fishing_spots_gdf = gpd.read_file(fishing_spots_url)
except Exception as e:
    st.error(f"Error loading GeoJSON data: {e}")
    water_quality_stations_gdf = None
    fishing_spots_gdf = None

with col1:
    # 建立 Leafmap 地圖
    m = leafmap.Map(
        locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
    )
    m.add_basemap(basemap)

    # 新增 GeoJSON 到地圖
    if water_quality_stations_gdf is not None:
        m.add_geojson(
            water_quality_stations_url,
            layer_name="Water Quality Stations",
        )

    if fishing_spots_gdf is not None:
        m.add_geojson(
            fishing_spots_url,
            layer_name="Fishing Spots",
        )

    # 顯示地圖於 Streamlit
    m.to_streamlit(height=800)

# 顯示 GeoJSON 屬性資料表
st.subheader("Water Quality Stations Data")
if water_quality_stations_gdf is not None:
    st.dataframe(water_quality_stations_gdf.head(10))  # 顯示前10筆資料

st.subheader("Fishing Spots Data")
if fishing_spots_gdf is not None:
    st.dataframe(fishing_spots_gdf.head(10))  # 顯示前10筆資料
