import streamlit as st
import leafmap.foliumap as leafmap

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
    basemap = st.selectbox("Select a basemap:", options, index)

with col1:
    m = leafmap.Map(
        locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
    )
    m.add_basemap(basemap)

    water_quality_stations_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E5%9F%9F%E6%B0%B4%E8%B3%AA%E6%B8%AC%E7%AB%99.geojson"
    fishing_spots_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E5%85%A8%E5%8F%B0%E9%96%8B%E6%94%BE%E9%87%A3%E9%BB%9E%E4%BD%8D%E7%BD%AE%20(1).geojson"
    fish_icon_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/fish-solid.svg"
    water_icon_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/droplet-solid.svg"
    
    m.add_geojson(
        water_quality_stations_url,
        layer_name="Water Quality Stations",
      )

    for feature in m.get_geojson_features(water_quality_stations_url):
        lat, lon = feature['geometry']['coordinates']
        icon = CustomIcon(icon_url=water_icon_url, icon_size=(30, 30))
        folium.Marker([lat, lon], icon=icon).add_to(m)
    
    m.add_geojson(
        fishing_spots_url,
        layer_name="Fishing Spots",
      )

    for feature in m.get_geojson_features(fishing_spots_url):
        lat, lon = feature['geometry']['coordinates']
        icon = CustomIcon(icon_url=fish_icon_url, icon_size=(30, 30))
        folium.Marker([lat, lon], icon=icon).add_to(m)
    
    m.to_streamlit(height=700)
