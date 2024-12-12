import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

st.set_page_config(layout="wide")

markdown = """
Web App URL: <https://geotemplate.streamlit.app>
GitHub Repository: <https://github.com/giswqs/streamlit-multipage-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("Marker Cluster")

with st.expander("See source code"):
    with st.echo():
        # 建立地圖
        m = leafmap.Map(center=[23.5, 121], zoom=7)

        water_quality_stations_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E5%9F%9F%E6%B0%B4%E8%B3%AA%E6%B8%AC%E7%AB%99.geojson"
        fishing_spots_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E5%85%A8%E5%8F%B0%E9%96%8B%E6%94%BE%E9%87%A3%E9%BB%9E%E4%BD%8D%E7%BD%AE%20(1).geojson"

        # 讀取 GeoJSON 資料
        water_quality_stations_gdf = gpd.read_file(water_quality_stations_url)
        fishing_spots_gdf = gpd.read_file(fishing_spots_url)

        # 確保 GeoDataFrame 包含正確的經緯度座標
        water_quality_stations_gdf["lon"] = water_quality_stations_gdf.geometry.x
        water_quality_stations_gdf["lat"] = water_quality_stations_gdf.geometry.y

        fishing_spots_gdf["lon"] = fishing_spots_gdf.geometry.x
        fishing_spots_gdf["lat"] = fishing_spots_gdf.geometry.y

        # 添加水質測站群集
        m.add_points_from_xy(
            water_quality_stations_gdf,
            x="lon",
            y="lat",
            color_column=None,  # 無需使用顏色分類
            spin=False,
            add_legend=False,
            layer_name="Water Quality Stations",
        )

        # 添加釣魚點群集
        m.add_points_from_xy(
            fishing_spots_gdf,
            x="lon",
            y="lat",
            color_column=None,  # 無需使用顏色分類
            spin=False,
            add_legend=False,
            layer_name="Fishing Spots",
        )

# 顯示地圖
m.to_streamlit(height=700)
