import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap

# 設定頁面布局
st.set_page_config(layout="wide")

# 讀取資料
county_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E7%B8%A3%E5%B8%82%E8%A8%88%E6%95%B8%E7%B5%90%E6%9E%9C4326.shp"
water_quality_stations_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E5%9F%9F%E6%B0%B4%E8%B3%AA%E6%B8%AC%E7%AB%99.geojson"
fishing_spots_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E5%85%A8%E5%8F%B0%E9%96%8B%E6%94%BE%E9%87%A3%E9%BB%9E%E4%BD%8D%E7%BD%AE%20(1).geojson"

# 讀取 SHP 文件
try:
    county_gdf = gpd.read_file(county_url).to_crs("EPSG:4326")
except Exception as e:
    st.error(f"載入 SHP 檔案時出現錯誤: {e}")
    county_gdf = None

# 讀取水質測站和釣魚點資料
try:
    water_quality_stations_gdf = gpd.read_file(water_quality_stations_url)
    fishing_spots_gdf = gpd.read_file(fishing_spots_url)
except Exception as e:
    st.error(f"載入 GeoJSON 資料時出現錯誤: {e}")
    water_quality_stations_gdf, fishing_spots_gdf = None, None

# 確認資料是否正確
if water_quality_stations_gdf is not None:
    st.success("成功載入水質測站資料")
    st.write(water_quality_stations_gdf.head())
if fishing_spots_gdf is not None:
    st.success("成功載入釣魚點資料")
    st.write(fishing_spots_gdf.head())

# 1. 點位地圖
st.subheader("1. 點位地圖")
m = leafmap.Map(locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
m.add_basemap("OpenTopoMap")
if county_gdf is not None:
    m.add_gdf(county_gdf, layer_name="縣市邊界")
if water_quality_stations_gdf is not None:
    m.add_gdf(water_quality_stations_gdf, layer_name="水質測站")
if fishing_spots_gdf is not None:
    m.add_gdf(fishing_spots_gdf, layer_name="釣魚點")
m.to_streamlit(height=400)

# 提供底圖選項
st.subheader("2. 多圖地圖顯示")
basemap_options = list(leafmap.basemaps.keys())

# 第一行地圖
st.write("### 第一行地圖")
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    basemap1 = st.selectbox("選擇左側地圖的底圖:", basemap_options, key="basemap1")
    m1 = leafmap.Map(center=[23.5, 121], zoom=8)
    m1.add_basemap(basemap1)
    if water_quality_stations_gdf is not None:
        m1.add_gdf(water_quality_stations_gdf, layer_name="水質測站")
    m1.to_streamlit(height=400)

with row1_col2:
    basemap2 = st.selectbox("選擇右側地圖的底圖:", basemap_options, key="basemap2")
    m2 = leafmap.Map(center=[23.5, 121], zoom=8)
    m2.add_basemap(basemap2)
    if fishing_spots_gdf is not None:
        m2.add_gdf(fishing_spots_gdf, layer_name="釣魚點")
    m2.to_streamlit(height=400)

# 屬性資料顯示
st.subheader("3. 屬性資料表")
if water_quality_stations_gdf is not None:
    st.write("水質測站資料")
    st.dataframe(water_quality_stations_gdf.head(10))
if fishing_spots_gdf is not None:
    st.write("釣魚點資料")
    st.dataframe(fishing_spots_gdf.head(10))
