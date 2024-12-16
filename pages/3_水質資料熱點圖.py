import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

# 設定 Streamlit 頁面配置
st.set_page_config(layout="wide")

# 側邊欄內容
markdown = """
Web App URL: <https://geotemplate.streamlit.app>
GitHub Repository: <https://github.com/giswqs/streamlit-multipage-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("Chemical Substance Heatmaps")

# 下載 GeoJSON 資料
url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/streamlit%E6%B0%B4%E8%B3%AA%E6%83%85%E6%B3%81.geojson"
data = gpd.read_file(url)

# 定義化學物質類別
heavy_metals = ['Cd', 'Cr', 'Cu', 'Zn', 'Pb', 'Hg']
organic_compounds = ['NO3_N', 'MI3PO4', 'NO2_N', 'SiO2']
suspended_solids = ['SS']

# 建立熱點圖函數
def create_heatmap(data, value_columns, title):
    st.subheader(title)
    m = leafmap.Map(center=[23.5, 121], zoom=7, tiles="stamen toner")  # 修正 tiles 為 "stamen toner" 並增加 attribution
    for value in value_columns:
        m.add_heatmap(
            data,
            latitude="LAT",
            longitude="LON",
            value=value,
            name=f"{value} Heatmap",
            radius=20,
        )
    m.to_streamlit(height=500)

# 重金屬熱點圖
create_heatmap(data, heavy_metals, "Heavy Metals Heatmap")

# 有機化合物熱點圖
create_heatmap(data, organic_compounds, "Organic Compounds Heatmap")

# 懸浮物質熱點圖
create_heatmap(data, suspended_solids, "Suspended Solids Heatmap")
