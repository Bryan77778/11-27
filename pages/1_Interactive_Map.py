import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap
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
st.title("Interactive Maps")

# 資料 URL
water_quality_stations_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E5%9F%9F%E6%B0%B4%E8%B3%AA%E6%B8%AC%E7%AB%99.geojson"
fishing_spots_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E5%85%A8%E5%8F%B0%E9%96%8B%E6%94%BE%E9%87%A3%E9%BB%9E%E4%BD%8D%E7%BD%AE%20(1).geojson"
county_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E7%B8%A3%E5%B8%82%E8%A8%88%E6%95%B8%E7%B5%90%E6%9E%9C.shp"

# 讀取資料
try:
    water_quality_stations_gdf = gpd.read_file(water_quality_stations_url).to_crs("EPSG:4326")
    fishing_spots_gdf = gpd.read_file(fishing_spots_url).to_crs("EPSG:4326")
    county_gdf = gpd.read_file(county_url).to_crs("EPSG:4326")
except Exception as e:
    st.error(f"Error loading data: {e}")
    water_quality_stations_gdf = None
    fishing_spots_gdf = None
    county_gdf = None

# 1. 點位地圖
st.subheader("1. 點位圖")
m = leafmap.Map(locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
m.add_basemap("OpenTopoMap")
if water_quality_stations_gdf is not None:
    m.add_geojson(water_quality_stations_url, layer_name="Water Quality Stations")
if fishing_spots_gdf is not None:
    m.add_geojson(fishing_spots_url, layer_name="Fishing Spots")
m.to_streamlit(height=400)

# 2. 水質測站數量 3D 面量圖
st.subheader("2. 水質測站數量 (3D)")
if county_gdf is not None:
    water_quality_layer = pdk.Layer(
        "ColumnLayer",
        data=county_gdf,
        get_position="[geometry.centroid.x, geometry.centroid.y]",
        get_elevation="WATER_COUNT",
        elevation_scale=100,
        radius=10000,
        get_fill_color="[0, 128, 255, 160]",
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
        tooltip={"html": "<b>County:</b> {COUNTYNAME}<br><b>Water Count:</b> {WATER_COUNT}"},
    )
    st.pydeck_chart(water_quality_map)

# 3. 釣魚點數量 3D 面量圖
st.subheader("3. 釣魚點數量 (3D)")
if county_gdf is not None:
    fishing_spots_layer = pdk.Layer(
        "ColumnLayer",
        data=county_gdf,
        get_position="[geometry.centroid.x, geometry.centroid.y]",
        get_elevation="FISH_COUNT",
        elevation_scale=100,
        radius=10000,
        get_fill_color="[255, 165, 0, 160]",
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
        tooltip={"html": "<b>County:</b> {COUNTYNAME}<br><b>Fish Count:</b> {FISH_COUNT}"},
    )
    st.pydeck_chart(fishing_spots_map)

# 顯示屬性資料表
st.subheader("Water Quality Stations Data")
if water_quality_stations_gdf is not None:
    st.dataframe(water_quality_stations_gdf.head(10))  # 顯示前10筆資料

st.subheader("Fishing Spots Data")
if fishing_spots_gdf is not None:
    st.dataframe(fishing_spots_gdf.head(10))  # 顯示前10筆資料
