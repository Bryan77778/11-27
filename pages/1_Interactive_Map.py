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
st.title("Interactive Maps")

# GeoJSON 和 Shapefile URL
water_quality_stations_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E5%9F%9F%E6%B0%B4%E8%B3%AA%E6%B8%AC%E7%AB%99.geojson"
fishing_spots_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E5%85%A8%E5%8F%B0%E9%96%8B%E6%94%BE%E9%87%A3%E9%BB%9E%E4%BD%8D%E7%BD%AE%20(1).geojson"
county_shp_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/COUNTY_MOI_1130718.shp"

# 使用 GeoPandas 讀取資料
try:
    water_quality_stations_gdf = gpd.read_file(water_quality_stations_url)
    fishing_spots_gdf = gpd.read_file(fishing_spots_url)
    county_gdf = gpd.read_file(county_shp_url)
except Exception as e:
    st.error(f"Error loading spatial data: {e}")
    water_quality_stations_gdf = None
    fishing_spots_gdf = None
    county_gdf = None

# 修正縣市名稱和統計數量
if water_quality_stations_gdf is not None:
    water_quality_stations_gdf.rename(columns={"Location": "county"}, inplace=True)
    water_quality_counts = water_quality_stations_gdf["county"].value_counts().reset_index()
    water_quality_counts.columns = ["county", "water_quality_count"]

if fishing_spots_gdf is not None:
    fishing_spots_gdf.rename(columns={"county": "county"}, inplace=True)
    fishing_spots_counts = fishing_spots_gdf["county"].value_counts().reset_index()
    fishing_spots_counts.columns = ["county", "fishing_spots_count"]

# 合併數量到 COUNTY 資料
if county_gdf is not None:
    county_gdf = county_gdf.to_crs("EPSG:4326")
    if water_quality_stations_gdf is not None:
        county_gdf = county_gdf.merge(water_quality_counts, on="county", how="left")
    if fishing_spots_gdf is not None:
        county_gdf = county_gdf.merge(fishing_spots_counts, on="county", how="left")
    county_gdf.fillna(0, inplace=True)  # 填充空值

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
if county_gdf is not None:
    water_quality_layer = pdk.Layer(
        "ColumnLayer",
        data=county_gdf,
        get_position=["geometry.centroid.x", "geometry.centroid.y"],
        get_elevation="water_quality_count",
        elevation_scale=100,
        radius=5000,
        get_fill_color="[0, 128, 255, 160]",
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=county_gdf.geometry.centroid.y.mean(),
        longitude=county_gdf.geometry.centroid.x.mean(),
        zoom=7,
        pitch=40,
    )

    water_quality_map = pdk.Deck(
        layers=[water_quality_layer],
        initial_view_state=view_state,
        tooltip={"html": "<b>County:</b> {county}<br><b>Water Quality Count:</b> {water_quality_count}"},
    )

    st.pydeck_chart(water_quality_map)

# 3. 縣市釣魚點數量 3D 化
st.subheader("3. 釣魚點數量 (3D)")
if county_gdf is not None:
    fishing_spots_layer = pdk.Layer(
        "ColumnLayer",
        data=county_gdf,
        get_position=["geometry.centroid.x", "geometry.centroid.y"],
        get_elevation="fishing_spots_count",
        elevation_scale=100,
        radius=5000,
        get_fill_color="[255, 165, 0, 160]",
        pickable=True,
    )

    fishing_spots_map = pdk.Deck(
        layers=[fishing_spots_layer],
        initial_view_state=view_state,
        tooltip={"html": "<b>County:</b> {county}<br><b>Fishing Spots Count:</b> {fishing_spots_count}"},
    )

    st.pydeck_chart(fishing_spots_map)

# 顯示屬性資料表
st.subheader("Water Quality Stations Data")
if water_quality_stations_gdf is not None:
    st.dataframe(water_quality_stations_gdf.head(10))  # 顯示前10筆資料

st.subheader("Fishing Spots Data")
if fishing_spots_gdf is not None:
    st.dataframe(fishing_spots_gdf.head(10))  # 顯示前10筆資料

st.subheader("COUNTY Data")
if county_gdf is not None:
    st.dataframe(county_gdf[["county", "water_quality_count", "fishing_spots_count"]])
