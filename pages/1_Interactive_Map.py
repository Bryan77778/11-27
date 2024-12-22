import streamlit as st
import geopandas as gpd
import pydeck as pdk
import leafmap.foliumap as leafmap

# 讀取資料
county_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E7%B8%A3%E5%B8%82%E8%A8%88%E6%95%B8%E7%B5%90%E6%9E%9C4326.shp"
water_quality_stations_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E5%9F%9F%E6%B0%B4%E8%B3%AA%E6%B8%AC%E7%AB%99.geojson"
fishing_spots_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E5%85%A8%E5%8F%B0%E9%96%8B%E6%94%BE%E9%87%A3%E9%BB%9E%E4%BD%8D%E7%BD%AE%20(1).geojson"

# 讀取 SHP 文件
try:
    county_gdf = gpd.read_file(county_url).to_crs("EPSG:4326")
except Exception as e:
    st.error(f"載入SHAPE檔案時出現錯誤: {e}")
    county_gdf = None

# 讀取水質測站和釣魚點資料
try:
    water_quality_stations_gdf = gpd.read_file(water_quality_stations_url)
    fishing_spots_gdf = gpd.read_file(fishing_spots_url)
except Exception as e:
    st.error(f"載入GeoJSON資料時出現錯誤: {e}")
    water_quality_stations_gdf = None
    fishing_spots_gdf = None

# 1. 點位地圖
st.subheader("1. 點位地圖")
m = leafmap.Map(locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
m.add_basemap("OpenTopoMap")
if water_quality_stations_gdf is not None:
    m.add_geojson(water_quality_stations_url, layer_name="水質測站")
if fishing_spots_gdf is not None:
    m.add_geojson(fishing_spots_url, layer_name="釣魚點")
if county_gdf is not None:
    m.add_geojson(county_url, layer_name="縣市邊界")
m.to_streamlit(height=400)

# 顯示水質測站資料表
st.subheader("水質測站資料")
if water_quality_stations_gdf is not None:
    st.dataframe(water_quality_stations_gdf.head(10))  # 顯示前10筆資料

# 顯示釣魚點資料表
st.subheader("釣魚點資料")
if fishing_spots_gdf is not None:
    st.dataframe(fishing_spots_gdf.head(10))  # 顯示前10筆資料
