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

# 資料 URL
water_quality_stations_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E5%9F%9F%E6%B0%B4%E8%B3%AA%E6%B8%AC%E7%AB%99.geojson"
fishing_spots_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E5%85%A8%E5%8F%B0%E9%96%8B%E6%94%BE%E9%87%A3%E9%BB%9E%E4%BD%8D%E7%BD%AE%20(1).geojson"
county_shp_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/COUNTY_MOI_1130718.shp"

# 讀取資料
try:
    water_quality_stations_gdf = gpd.read_file(water_quality_stations_url)
    fishing_spots_gdf = gpd.read_file(fishing_spots_url)
    county_gdf = gpd.read_file(county_shp_url)
except Exception as e:
    st.error(f"Error loading data: {e}")
    water_quality_stations_gdf = None
    fishing_spots_gdf = None
    county_gdf = None

# 確保坐標系統一致
if water_quality_stations_gdf is not None:
    water_quality_stations_gdf = water_quality_stations_gdf.to_crs("EPSG:4326")
if fishing_spots_gdf is not None:
    fishing_spots_gdf = fishing_spots_gdf.to_crs("EPSG:4326")
if county_gdf is not None:
    county_gdf = county_gdf.to_crs("EPSG:4326")

# 將 Location 欄位改名為 county
if water_quality_stations_gdf is not None and "Location" in water_quality_stations_gdf.columns:
    water_quality_stations_gdf.rename(columns={"Location": "county"}, inplace=True)

if fishing_spots_gdf is not None and "county" not in fishing_spots_gdf.columns:
    fishing_spots_gdf["county"] = fishing_spots_gdf["county"]  # 確保有 county 欄位

# 計算點位數量並合併到縣市圖層
if county_gdf is not None:
    # 計算水質測站數量
    if water_quality_stations_gdf is not None:
        water_quality_counts = water_quality_stations_gdf["county"].value_counts().reset_index()
        water_quality_counts.columns = ["county", "water_quality_count"]
        county_gdf = county_gdf.merge(water_quality_counts, on="county", how="left")
        county_gdf["water_quality_count"] = county_gdf["water_quality_count"].fillna(0)

    # 計算釣魚點數量
    if fishing_spots_gdf is not None:
        fishing_spots_counts = fishing_spots_gdf["county"].value_counts().reset_index()
        fishing_spots_counts.columns = ["county", "fishing_spots_count"]
        county_gdf = county_gdf.merge(fishing_spots_counts, on="county", how="left")
        county_gdf["fishing_spots_count"] = county_gdf["fishing_spots_count"].fillna(0)

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
        get_position="[geometry.x, geometry.y]",
        get_elevation="water_quality_count",
        elevation_scale=100,
        radius=5000,
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
        tooltip={"html": "<b>County:</b> {county}<br><b>Count:</b> {water_quality_count}"},
    )

    st.pydeck_chart(water_quality_map)

# 3. 縣市釣魚點數量 3D 化
st.subheader("3. 釣魚點數量 (3D)")
if county_gdf is not None:
    fishing_spots_layer = pdk.Layer(
        "ColumnLayer",
        data=county_gdf,
        get_position="[geometry.x, geometry.y]",
        get_elevation="fishing_spots_count",
        elevation_scale=100,
        radius=5000,
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
        tooltip={"html": "<b>County:</b> {county}<br><b>Count:</b> {fishing_spots_count}"},
    )

    st.pydeck_chart(fishing_spots_map)

# 屬性資料表顯示
st.subheader("County Data")
if county_gdf is not None:
    st.dataframe(county_gdf[["county", "water_quality_count", "fishing_spots_count"]])
