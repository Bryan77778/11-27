import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("Split-panel Map(尚未成功)")

with st.expander("See source code"):
    with st.echo():
        water_quality_stations_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E5%9F%9F%E6%B0%B4%E8%B3%AA%E6%B8%AC%E7%AB%99.geojson"
        fishing_spots_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E5%85%A8%E5%8F%B0%E9%96%8B%E6%94%BE%E9%87%A3%E9%BB%9E%E4%BD%8D%E7%BD%AE%20(1).geojson"

        left_map = leafmap.Map(center=[23.5, 121], zoom=5) 
        left_map.add_geojson(
            water_quality_stations_url,
            layer_name="Water Quality Stations",
        )
            
        right_map = leafmap.Map(center=[23.5, 121], zoom=10)
        right_map.add_geojson(
            fishing_spots_url,
            layer_name="Fishing Spots",
        )

        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### 左側地圖：水質測站")
            left_map.to_streamlit(height=700)

        with col2:
            st.write("### 右側地圖：釣魚點")
            right_map.to_streamlit(height=700)
