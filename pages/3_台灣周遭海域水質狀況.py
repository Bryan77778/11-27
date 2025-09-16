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
    <style>
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
                          url('https://github.com/Bryan77778/11-27/blob/main/%E8%83%8C%E6%99%AF%E5%9C%96%E7%89%87.png?raw=true'); /* 添加半透明黑色遮罩 */
        background-size: cover; /* 背景圖片填滿窗口 */
        background-position: center; /* 背景圖片居中 */
        color: white; /* 全局字體顏色設置為白色 */
    }
    .custom-text {
        font-size: 18px; /* 設置文字大小 */
        line-height: 1.6; /* 行距 */
        color: white; /* 設置文字顏色 */
    }
    .stSelectbox div[role="combobox"] {
        color: white;  /* 下拉選單內的文字設置為黑色（避免與白色背景衝突） */
        background-color: white;  /* 下拉選單背景設置為白色 */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="custom-text">
    - 化學元素會以熱點圖的形式呈現，分別有重金屬、有機化合物、懸浮物質 \n
    - 圖台右上方可勾選以呈現不同的化學元素 \n
    - 屬性資料表展示化學元素數值 \n
    - 當測站中的元素數值大於90%時，會被視為離群測站 \n
    - 某個化學元素離群測站超過五個會被繪製成直方圖 \n
    - 可用於參考海域水質情況 \n
    - **重金屬**：Cd 鎘, Cr 鉻, Cu 銅, Zn 鋅, Pb 鉛, Hg 汞 \n
    - **有機化合物**：NO3_N 硝酸氮, MI3PO4 磷酸鹽, NO2_N 亞硝酸氮, SiO2 二氧化矽 \n
    - **懸浮固體**：SS 二氧化矽 \n
    </div>
    """,
    unsafe_allow_html=True
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
heavy_metals = ['Cd', 'Cr', 'Cu', 'Zn', 'Pb', 'Hg']
organic_compounds = ['NO3_N', 'MI3PO4', 'NO2_N', 'SiO2']
suspended_solids = ['SS']

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
    st.dataframe(data[["STATION_NAME", "LAT", "LON"] + value_columns].round(5))

    # 分位數法檢測離群值並顯示結果
    st.write(f"Outlier Detection for {title}")
    for value in value_columns:
        # 計算 90 百分位數的上界值，取到小數點後五位
        upper_bound = round(np.percentile(data[value].dropna(), 90), 5)
        outliers = data[data[value] > upper_bound]

        # 顯示離群測站結果
        if len(outliers) >= 5:
            st.write(f"{value} 的離群測站: {len(outliers)} 個")
            st.dataframe(outliers[["STATION_NAME", "LAT", "LON", value]].round(5))
            
            # 顯示長條圖
            st.bar_chart(outliers.set_index("STATION_NAME")[value])
            st.write(f"{value} 的上界值（90百分位數）: {upper_bound}")
            st.write("--------------------")
        else:
            st.write(f"{value} 的離群測站數量不足 5 個，無法繪製直方圖。")
            st.write(f"{value} 的上界值（90百分位數）: {upper_bound}")
            st.write("--------------------")

# 重金屬熱點圖
create_heatmap(data, heavy_metals, "重金屬熱點圖")

# 有機化合物熱點圖
create_heatmap(data, organic_compounds, "有機化合物熱點圖")

# 懸浮物質熱點圖
create_heatmap(data, suspended_solids, "懸浮物質熱點圖")
