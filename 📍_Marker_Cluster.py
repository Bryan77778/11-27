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

        # 添加地理數據
        m.add_geojson(water_quality_stations_url, layer_name='Water Quality Stations')
        m.add_geojson(fishing_spots_url, layer_name='Fishing Spots')

        # 如果需要對兩個 GeoJSON 文件中的點進行樣式設定：
        # m.add_points_from_xy(), 顏色、圖示等可依需求設定。

# 將地圖顯示於 Streamlit
m.to_streamlit(height=700)
