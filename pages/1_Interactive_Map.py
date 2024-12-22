import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap

# 設定頁面布局
st.set_page_config(layout="wide")

# 資料來源
county_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E7%B8%A3%E5%B8%82%E8%A8%88%E6%95%B8%E7%B5%90%E6%9E%9C4326.shp"
water_quality_stations_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E5%9F%9F%E6%B0%B4%E8%B3%AA%E6%B8%AC%E7%AB%99.geojson"
fishing_spots_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E5%85%A8%E5%8F%B0%E9%96%8B%E6%94%BE%E9%87%A3%E9%BB%9E%E4%BD%8D%E7%BD%AE%20(1).geojson"

# 讀取資料
try:
    county_gdf = gpd.read_file(county_url).to_crs("EPSG:4326")
    water_quality_stations_gdf = gpd.read_file(water_quality_stations_url)
    fishing_spots_gdf = gpd.read_file(fishing_spots_url)
except Exception as e:
    st.error(f"資料讀取錯誤: {e}")
    county_gdf, water_quality_stations_gdf, fishing_spots_gdf = None, None, None

# 提供底圖選項
basemap_options = list(leafmap.basemaps.keys())
default_basemap = "OpenTopoMap"

# 一、點位地圖呈現
st.subheader("一、點位地圖呈現")
selected_basemap = st.selectbox("選擇點位地圖的底圖", basemap_options, index=basemap_options.index(default_basemap))
m = leafmap.Map(locate_control=True, zoom=8, latlon_control=True, draw_export=True, minimap_control=True)
m.add_basemap(selected_basemap)
if county_gdf is not None:
    m.add_gdf(county_gdf, layer_name="縣市邊界")
if water_quality_stations_gdf is not None:
    m.add_gdf(water_quality_stations_gdf, layer_name="水質測站")
if fishing_spots_gdf is not None:
    m.add_gdf(fishing_spots_gdf, layer_name="釣魚點")
m.to_streamlit(height=500)

# 二、釣魚點與測站地圖並排呈現
st.subheader("二、釣魚點與測站地圖並排呈現")
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.write("### 左側地圖：水質測站點位地圖")
    basemap1 = st.selectbox("選擇水質測站地圖的底圖", basemap_options, key="map1", index=basemap_options.index(default_basemap))
    m1 = leafmap.Map(center=[23.5, 121], zoom=8)
    m1.add_basemap(basemap1)
    if water_quality_stations_gdf is not None:
        m1.add_gdf(water_quality_stations_gdf, layer_name="水質測站")
    m1.to_streamlit(height=500)

with row1_col2:
    st.write("### 右側地圖：釣魚點點位地圖")
    basemap2 = st.selectbox("選擇釣魚點地圖的底圖", basemap_options, key="map2", index=basemap_options.index(default_basemap))
    m2 = leafmap.Map(center=[23.5, 121], zoom=8)
    m2.add_basemap(basemap2)
    if fishing_spots_gdf is not None:
        m2.add_gdf(fishing_spots_gdf, layer_name="釣魚點")
    m2.to_streamlit(height=500)

# 三、釣魚點與測站群集地圖並排呈現
st.subheader("三、釣魚點與測站群集地圖並排呈現")
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.write("### 左側地圖：水質測站群集地圖")
    basemap3 = st.selectbox("選擇水質測站群集地圖的底圖", basemap_options, key="map3", index=basemap_options.index(default_basemap))
    m3 = leafmap.Map(center=[23.5, 121], zoom=8)
    m3.add_basemap(basemap3)
    if water_quality_stations_gdf is not None:
        m3.add_points_from_xy(
            water_quality_stations_gdf,
            x="LON",  # 確認實際欄位名稱
            y="LAT",  # 確認實際欄位名稱
            cluster=True,
            layer_name="水質測站群集",
        )
    m3.to_streamlit(height=500)

with row2_col2:
    st.write("### 右側地圖：釣魚點群集地圖")
    basemap4 = st.selectbox("選擇釣魚點群集地圖的底圖", basemap_options, key="map4", index=basemap_options.index(default_basemap))
    m4 = leafmap.Map(center=[23.5, 121], zoom=8)
    m4.add_basemap(basemap4)
    if fishing_spots_gdf is not None:
        m4.add_points_from_xy(
            fishing_spots_gdf,
            x="XPOS",  # 確認實際欄位名稱
            y="YPOS",  # 確認實際欄位名稱
            cluster=True,
            layer_name="釣魚點群集",
        )
    m4.to_streamlit(height=500)

# 四、釣魚點與測站的屬性資料表
st.subheader("四、釣魚點與測站的屬性資料表")
if water_quality_stations_gdf is not None:
    st.write("#### 水質測站屬性資料表")
    st.dataframe(water_quality_stations_gdf.head(10))

if fishing_spots_gdf is not None:
    st.write("#### 釣魚點屬性資料表")
    st.dataframe(fishing_spots_gdf.head(10))
