import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import pandas as pd
import numpy as np

# 設定 Streamlit 頁面配置
st.set_page_config(layout="wide")
st.title("台灣周遭海域水質狀況")
st.markdown(
"""
- 化學元素會以熱點圖的形式呈現，分別有重金屬、有機化合物、懸浮物質
- 圖台右上方可勾選以呈現不同的化學元素
- 屬性資料表展示化學元素數值
- 當測站中的元素數值大於90%時，會被視為離群測站
- 某個化學元素離群測站超過五個會被繪製成直方圖
- 可用於參考海域水質情況
"""
)
# 側邊欄內容
markdown = """
Web App URL: <https://geotemplate.streamlit.app>
GitHub Repository: <https://github.com/giswqs/streamlit-multipage-template>
"""
st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

# 下載 GeoJSON 資料
url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/streamlit%E6%B0%B4%E8%B3%AA%E6%83%85%E6%B3%81.geojson"
data = gpd.read_file(url)

# 定義化學物質類別
heavy_metals = ['Cd鎘', 'Cr鉻', 'Cu銅', 'Zn鋅', 'Pb鉛', 'Hg汞']
organic_compounds = ['NO3_N硝酸氮', 'MI3PO4磷酸鹽', 'NO2_N亞硝酸氮', 'SiO2二氧化矽']
suspended_solids = ['SS二氧化矽']

# 建立熱點圖函數
def create_heatmap(data, value_columns, title):
    st.subheader(title)
    m = leafmap.Map(center=[23.5, 121], zoom=7)

    # 加入測站點位，並顯示水質數值的彈出視窗
    m.add_points_from_xy(
        data,
        x="LON",
        y="LAT",
        color_column=None,
        popup=["STATION_NAME", "TYPE"] + value_columns
    )

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

    # 在地圖下方顯示屬性資料表
    st.write(f"{title}數值")
    st.dataframe(data[["STATION_NAME", "LAT", "LON"] + value_columns])

    # 分位數法檢測離群值並顯示結果
    st.write(f"Outlier Detection for {title}")
    for value in value_columns:
        upper_bound = np.percentile(data[value].dropna(), 90)
        outliers = data[data[value] > upper_bound]
        
        # 檢查離群測站數量是否 >= 5
        if len(outliers) >= 5:
            st.write(f"{value} 的離群測站: {len(outliers)} 個")
            st.dataframe(outliers[["STATION_NAME", "LAT", "LON", value]])
            
            # 顯示長條圖
            st.bar_chart(outliers.set_index("STATION_NAME")[value])
            st.write(f"{value} 的上界值（90百分位數）: {upper_bound}")
            st.write("--------------------")
        else:
            st.write(f"{value} 的離群測站數量不足 5 個，無法繪製直方圖。")
            st.write("--------------------")
# 重金屬熱點圖
create_heatmap(data, heavy_metals, "重金屬熱點圖")

# 有機化合物熱點圖
create_heatmap(data, organic_compounds, "有機化合物熱點圖")

# 懸浮物質熱點圖
create_heatmap(data, suspended_solids, "懸浮物質熱點圖")
