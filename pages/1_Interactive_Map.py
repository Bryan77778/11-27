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

# 計算各縣市的點位數量與中心點座標
def prepare_count_data(gdf):
    # 確保座標系統正確
    gdf = gdf.to_crs("EPSG:4326")
    # 計算縣市名稱及其點數
    county_counts = gdf.groupby("COUNTY").size().reset_index(name="count")
    # 計算各縣市中心點
    centroids = gdf.dissolve(by="COUNTY").centroid.reset_index()
    # 合併中心點與點數
    county_counts = county_counts.merge(centroids, on="COUNTY")
    # 轉換座標為經緯度
    county_counts["lon"] = county_counts.geometry.x
    county_counts["lat"] = county_counts.geometry.y
    return county_counts

# 處理水質測站資料
if water_quality_stations_gdf is not None:
    county_counts_wq = prepare_count_data(water_quality_stations_gdf)

# 處理釣魚點資料
if fishing_spots_gdf is not None:
    county_counts_fs = prepare_count_data(fishing_spots_gdf)

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
        get_position=["lon", "lat"],
        get_elevation="count",
        elevation_scale=100,
        radius=5000,
        get_fill_color="[0, 128, 255, 160]",
        pickable=True,
    )

    water_quality_view_state = pdk.ViewState(
        latitude=county_counts_wq["lat"].mean(),
        longitude=county_counts_wq["lon"].mean(),
        zoom=7,
        pitch=40,
    )

    water_quality_map = pdk.Deck(
        layers=[water_quality_layer],
        initial_view_state=water_quality_view_state,
        tooltip={"html": "<b>County:</b> {COUNTY}<br><b>Count:</b> {count}"},
    )

    st.pydeck_chart(water_quality_map)

# 3. 縣市釣魚點數量 3D 化
st.subheader("3. 釣魚點數量 (3D)")
if fishing_spots_gdf is not None:
    fishing_spots_layer = pdk.Layer(
        "ColumnLayer",
        data=county_counts_fs,
        get_position=["lon", "lat"],
        get_elevation="count",
        elevation_scale=100,
        radius=5000,
        get_fill_color="[255, 165, 0, 160]",
        pickable=True,
    )

    fishing_spots_view_state = pdk.ViewState(
        latitude=county_counts_fs["lat"].mean(),
        longitude=county_counts_fs["lon"].mean(),
        zoom=7,
        pitch=40,
    )

    fishing_spots_map = pdk.Deck(
        layers=[fishing_spots_layer],
        initial_view_state=fishing_spots_view_state,
        tooltip={"html": "<b>County:</b> {COUNTY}<br><b>Count:</b> {count}"},
    )

    st.pydeck_chart(fishing_spots_map)

# 顯示屬性資料表
st.subheader("Water Quality Stations Data")
if water_quality_stations_gdf is not None:
    st.dataframe(water_quality_stations_gdf.head(10))  # 顯示前10筆資料

st.subheader("Fishing Spots Data")
if fishing_spots_gdf is not None:
    st.dataframe(fishing_spots_gdf.head(10))  # 顯示前10筆資料
st.subheader("Fishing Spots Data")
if fishing_spots_gdf is not None:
    st.dataframe(fishing_spots_gdf.head(10))  # 顯示前10筆資料
