import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import pydeck as pdk

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
st.title("Interactive 3D Maps")

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

# 計算各縣市點位數量
if water_quality_stations_gdf is not None:
    water_quality_stations_gdf = water_quality_stations_gdf.to_crs("EPSG:4326")
    water_quality_stations_gdf["county"] = water_quality_stations_gdf.geometry.apply(lambda x: x.y)  # 假設已經有對應縣市的資料
    county_counts_wq = water_quality_stations_gdf["county"].value_counts().reset_index()
    county_counts_wq.columns = ["county", "count"]

if fishing_spots_gdf is not None:
    fishing_spots_gdf = fishing_spots_gdf.to_crs("EPSG:4326")
    fishing_spots_gdf["county"] = fishing_spots_gdf.geometry.apply(lambda x: x.y)  # 假設已經有對應縣市的資料
    county_counts_fs = fishing_spots_gdf["county"].value_counts().reset_index()
    county_counts_fs.columns = ["county", "count"]

# 1. 點位地圖
st.subheader("1. 點位地圖")
m = leafmap.Map(locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
m.add_basemap("OpenTopoMap")
if water_quality_stations_gdf is not None:
    m.add_geojson(water_quality_stations_url, layer_name="Water Quality Stations")
if fishing_spots_gdf is not None:
    m.add_geojson(fishing_spots_url, layer_name="Fishing Spots")
m.to_streamlit(height=400)

# 2. 縣市水質測站數量 3D 化
st.subheader("2. 水質測站數量 (3D)")
if water_quality_stations_gdf is not None:
    water_quality_layer = pdk.Layer(
        "ColumnLayer",
        data=county_counts_wq,
        get_position="[geometry.x, geometry.y]",
        get_elevation="count",
        elevation_scale=100,
        radius=5000,
        get_fill_color="[0, 128, 255, 160]",
        pickable=True,
    )

    water_quality_view_state = pdk.ViewState(
        latitude=water_quality_stations_gdf.geometry.y.mean(),
        longitude=water_quality_stations_gdf.geometry.x.mean(),
        zoom=7,
        pitch=40,
    )

    water_quality_map = pdk.Deck(
        layers=[water_quality_layer],
        initial_view_state=water_quality_view_state,
        tooltip={"html": "<b>County:</b> {county}<br><b>Count:</b> {count}"},
    )

    st.pydeck_chart(water_quality_map)

# 3. 縣市釣魚點數量 3D 化
st.subheader("3. 釣魚點數量 (3D)")
if fishing_spots_gdf is not None:
    fishing_spots_layer = pdk.Layer(
        "ColumnLayer",
        data=county_counts_fs,
        get_position="[geometry.x, geometry.y]",
        get_elevation="count",
        elevation_scale=100,
        radius=5000,
        get_fill_color="[255, 165, 0, 160]",
        pickable=True,
    )

    fishing_spots_view_state = pdk.ViewState(
        latitude=fishing_spots_gdf.geometry.y.mean(),
        longitude=fishing_spots_gdf.geometry.x.mean(),
        zoom=7,
        pitch=40,
    )

    fishing_spots_map = pdk.Deck(
        layers=[fishing_spots_layer],
        initial_view_state=fishing_spots_view_state,
        tooltip={"html": "<b>County:</b> {county}<br><b>Count:</b> {count}"},
    )

    st.pydeck_chart(fishing_spots_map)

# 顯示屬性資料表
st.subheader("Water Quality Stations Data")
if water_quality_stations_gdf is not None:
    st.dataframe(water_quality_stations_gdf.head(10))  # 顯示前10筆資料

st.subheader("Fishing Spots Data")
if fishing_spots_gdf is not None:
    st.dataframe(fishing_spots_gdf.head(10))  # 顯示前10筆資料
