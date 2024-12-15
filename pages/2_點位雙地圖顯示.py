import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

st.set_page_config(layout="wide")

markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("多圖地圖顯示")

# 讀取資料
water_quality_stations_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E5%9F%9F%E6%B0%B4%E8%B3%AA%E6%B8%AC%E7%AB%99.geojson"
fishing_spots_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E5%85%A8%E5%8F%B0%E9%96%8B%E6%94%BE%E9%87%A3%E9%BB%9E%E4%BD%8D%E7%BD%AE%20(1).geojson"

# 提供底圖選項
basemap_options = list(leafmap.basemaps.keys())

# 第一行地圖
st.write("### 第一行地圖")
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    basemap1 = st.selectbox("選擇左側地圖的底圖:", basemap_options, index=basemap_options.index("OpenStreetMap"))
    st.write("#### 左側地圖：水質測站 (Marker Cluster)")
    m1 = leafmap.Map(center=[23.5, 121], zoom=8)
    m1.add_basemap(basemap1)
    m1.add_geojson(water_quality_stations_url, layer_name="Water Quality Stations")
    m1.to_streamlit(height=500)

with row1_col2:
    basemap2 = st.selectbox("選擇右側地圖的底圖:", basemap_options, index=basemap_options.index("OpenStreetMap"))
    st.write("#### 右側地圖：釣魚點 (Marker Cluster)")
    m2 = leafmap.Map(center=[23.5, 121], zoom=8)
    m2.add_basemap(basemap2)
    m2.add_geojson(fishing_spots_url, layer_name="Fishing Spots")
    m2.to_streamlit(height=500)

# 第二行地圖
st.write("### 第二行地圖")
row2_col1, row2_col2 = st.columns(2)

# 使用 Geopandas 讀取資料
try:
    water_quality_stations_gdf = gpd.read_file(water_quality_stations_url)
    fishing_spots_gdf = gpd.read_file(fishing_spots_url)
except Exception as e:
    st.error(f"Error loading GeoJSON data: {e}")
    water_quality_stations_gdf = None
    fishing_spots_gdf = None

with row2_col1:
    basemap3 = st.selectbox("選擇左下地圖的底圖:", basemap_options, index=basemap_options.index("OpenStreetMap"))
    st.write("#### 左側地圖：水質測站 (聚合點圖)")
    m3 = leafmap.Map(center=[23.5, 121], zoom=8)
    m3.add_basemap(basemap3)
    if water_quality_stations_gdf is not None:
        m3.add_points_from_xy(
            water_quality_stations_gdf,
            x="LON",  # 根據實際資料調整欄位名稱
            y="LAT",  # 根據實際資料調整欄位名稱
            spin=True,
            add_legend=True,
            layer_name="水質監測站",
        )
    m3.to_streamlit(height=500)

with row2_col2:
    basemap4 = st.selectbox("選擇右下地圖的底圖:", basemap_options, index=basemap_options.index("OpenStreetMap"))
    st.write("#### 右側地圖：釣魚點 (聚合點圖)")
    m4 = leafmap.Map(center=[23.5, 121], zoom=8)
    m4.add_basemap(basemap4)
    if fishing_spots_gdf is not None:
        m4.add_points_from_xy(
            fishing_spots_gdf,
            x="XPOS",  # 根據實際資料調整欄位名稱
            y="YPOS",  # 根據實際資料調整欄位名稱
            spin=True,
            add_legend=True,
            layer_name="釣魚點",
        )
    m4.to_streamlit(height=500)

