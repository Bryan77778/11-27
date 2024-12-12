import streamlit as st
import leafmap.foliumap as leafmap

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

        # 新的資料路徑
        water_quality_stations_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E5%9F%9F%E6%B0%B4%E8%B3%AA%E6%B8%AC%E7%AB%99.geojson"
        fishing_spots_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E5%85%A8%E5%8F%B0%E9%96%8B%E6%94%BE%E9%87%A3%E9%BB%9E%E4%BD%8D%E7%BD%AE%20(1).geojson"

        # 讀取水質測站資料，轉換為 DataFrame
        water_quality_stations = leafmap.read_geojson(water_quality_stations_url)
        fishing_spots = leafmap.read_geojson(fishing_spots_url)

        # 添加水質測站群集
        m.add_points_from_xy(
            water_quality_stations,
            x="geometry.x",
            y="geometry.y",
            popup=["STATION_NAME"],  # 替換為 GeoJSON 中的相關欄位
            icon_colors=["blue"],  # 可設置點顏色
            layer_name="Water Quality Stations"
        )

        # 添加釣魚點群集
        m.add_points_from_xy(
            fishing_spots,
            x="geometry.x",
            y="geometry.y",
            popup=["name"],  # 替換為釣魚點相關欄位
            icon_colors=["green"],  # 可設置點顏色
            layer_name="Fishing Spots"
        )

# 顯示地圖
m.to_streamlit(height=700)
