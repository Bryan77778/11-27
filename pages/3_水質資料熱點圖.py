import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 設定 Streamlit 頁面配置
st.set_page_config(layout="wide")

# 側邊欄內容
markdown = """
Web App URL: <https://geotemplate.streamlit.app>
GitHub Repository: <https://github.com/giswqs/streamlit-multipage-template>
"""

st.sidebar.title("關於本網站")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("測站水質熱點圖")

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
    m = leafmap.Map(center=[23.5, 121], zoom=7)

    # 加入測站點位，顯示水質數值
    m.add_points_from_xy(
        data,
        x="LON",
        y="LAT",
        color_column=None,
        popup=["STATION_NAME", "TYPE"] + value_columns
    )

    # 加入熱點圖
    for value in value_columns:
        m.add_heatmap(
            data,
            latitude="LAT",
            longitude="LON",
            value=value,
            name=f"{value} 熱點圖",
            radius=20,
        )

    m.to_streamlit(height=500)

    # 顯示屬性數據表格
    st.write(f"**{title} 數值表格**")
    st.dataframe(data[["STATION_NAME", "LAT", "LON"] + value_columns])

    # 離群值檢測並繪製直方圖
    for value in value_columns:
        st.write(f"### {value} 數值分布與離群值檢測")

        # 計算 90 分位數
        upper_bound = np.percentile(data[value].dropna(), 90)
        outliers = data[data[value] > upper_bound]

        # 離群值表格
        st.write(f"**{value} 的離群測站數量: {len(outliers)} 個**")
        st.dataframe(outliers[["STATION_NAME", "LAT", "LON", value]])

        # 繪製直方圖
        fig, ax = plt.subplots(figsize=(1, 0.5))
        ax.hist(data[value].dropna(), bins=20, color='royalblue', edgecolor='black', alpha=0.7)
        ax.axvline(upper_bound, color='red', linestyle='dashed', linewidth=2, label=f"90% 分位數: {upper_bound:.4f}")
        ax.set_title(f"{value} 直方圖", fontsize=12)
        ax.set_xlabel("濃度數值", fontsize=10)
        ax.set_ylabel("測站數量", fontsize=10)
        ax.legend()

        # 顯示直方圖於 Streamlit
        st.pyplot(fig)

        # 顯示分位數上界值
        st.write(f"**{value} 的 90% 分位數上界值: {upper_bound:.4f}**")
        st.write("---")

# 重金屬熱點圖
create_heatmap(data, heavy_metals, "重金屬熱點圖")

# 有機化合物熱點圖
create_heatmap(data, organic_compounds, "有機化合物熱點圖")

# 懸浮物質熱點圖
create_heatmap(data, suspended_solids, "懸浮物質熱點圖")

