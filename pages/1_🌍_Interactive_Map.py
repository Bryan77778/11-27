import streamlit as st
import leafmap.foliumap as leafmap
import folium
from folium import CustomIcon
import geopandas as gpd

markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("Interactive Map")

col1, col2 = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("OpenTopoMap")

with col2:
    basemap = st.selectbox("Select a basemap:", ["OpenStreetMap", "OpenTopoMap"], index=0)

with col1:
    # 建立 Folium 地圖
    m = folium.Map(location=[23.5, 121], zoom_start=7, tiles=basemap.lower())

    # 資料來源 URL
    water_quality_stations_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E5%9F%9F%E6%B0%B4%E8%B3%AA%E6%B8%AC%E7%AB%99.geojson"
    fishing_spots_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E5%85%A8%E5%8F%B0%E9%96%8B%E6%94%BE%E9%87%A3%E9%BB%9E%E4%BD%8D%E7%BD%AE%20(1).geojson"
    fish_icon_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/fish-solid.svg"
    water_icon_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/droplet-solid.svg"

    # 載入 GeoJSON 並添加圖示
    water_quality_stations = gpd.read_file(water_quality_stations_url)
    for _, row in water_quality_stations.iterrows():
        lat, lon = row.geometry.y, row.geometry.x
        icon = CustomIcon(water_icon_url, icon_size=(30, 30))
        folium.Marker(location=[lat, lon], icon=icon).add_to(m)

    fishing_spots = gpd.read_file(fishing_spots_url)
    for _, row in fishing_spots.iterrows():
        lat, lon = row.geometry.y, row.geometry.x
        icon = CustomIcon(fish_icon_url, icon_size=(30, 30))
        folium.Marker(location=[lat, lon], icon=icon).add_to(m)

    # 在 Streamlit 中顯示地圖
    from streamlit_folium import st_folium
    st_folium(m, width=800, height=600)
