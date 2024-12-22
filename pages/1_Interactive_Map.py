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

# 2. 水質測站數量 3D 化
st.subheader("2. 水質測站數量 (3D)")
if county_gdf is not None:
    # 水質測站數量 3D 顯示
    water_quality_layer = pdk.Layer(
        "ColumnLayer",
        data=county_gdf,
        get_position=["geometry.centroid.x", "geometry.centroid.y"],  # 使用縣市重心點
        get_elevation="WATER_COUNT",  # 使用水質測站數量作為高度
        elevation_scale=100,  # 調整高度比例
        radius=5000,  # 調整圓柱半徑
        get_fill_color="[0, 128, 255, 160]",  # 顏色為藍色
        pickable=True,
    )

    water_quality_view_state = pdk.ViewState(
        latitude=county_gdf.geometry.centroid.y.mean(),
        longitude=county_gdf.geometry.centroid.x.mean(),
        zoom=7,
        pitch=40,
    )

    water_quality_map = pdk.Deck(
        layers=[water_quality_layer],
        initial_view_state=water_quality_view_state,
        tooltip={"html": "<b>縣市:</b> {COUNTYNAME}<br><b>水質測站數量:</b> {WATER_COUNT}"},
    )

    st.pydeck_chart(water_quality_map)

# 3. 釣魚點數量 3D 化
st.subheader("3. 釣魚點數量 (3D)")
if county_gdf is not None:
    # 釣魚點數量 3D 顯示
    fishing_spots_layer = pdk.Layer(
        "ColumnLayer",
        data=county_gdf,
        get_position=["geometry.centroid.x", "geometry.centroid.y"],  # 使用縣市重心點
        get_elevation="FISH_COUNT",  # 使用釣魚點數量作為高度
        elevation_scale=100,  # 調整高度比例
        radius=5000,  # 調整圓柱半徑
        get_fill_color="[255, 165, 0, 160]",  # 顏色為橙色
        pickable=True,
    )

    fishing_spots_view_state = pdk.ViewState(
        latitude=county_gdf.geometry.centroid.y.mean(),
        longitude=county_gdf.geometry.centroid.x.mean(),
        zoom=7,
        pitch=40,
    )

    fishing_spots_map = pdk.Deck(
        layers=[fishing_spots_layer],
        initial_view_state=fishing_spots_view_state,
        tooltip={"html": "<b>縣市:</b> {COUNTYNAME}<br><b>釣魚點數量:</b> {FISH_COUNT}"},
    )

    st.pydeck_chart(fishing_spots_map)

# 顯示水質測站資料表
st.subheader("水質測站資料")
if water_quality_stations_gdf is not None:
    st.dataframe(water_quality_stations_gdf.head(10))  # 顯示前10筆資料

# 顯示釣魚點資料表
st.subheader("釣魚點資料")
if fishing_spots_gdf is not None:
    st.dataframe(fishing_spots_gdf.head(10))  # 顯示前10筆資料

# 顯示縣市水質測站與釣魚點的屬性資料表
st.subheader("縣市水質測站與釣魚點資料")
if county_gdf is not None:
    st.dataframe(county_gdf[["COUNTYNAME", "WATER_COUNT", "FISH_COUNT"]].head(10))  # 顯示前10筆資料
