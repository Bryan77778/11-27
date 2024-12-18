import streamlit as st
import pandas as pd
import json
import leafmap.foliumap as leafmap
from streamlit_folium import st_folium

# 固定 Windy API Key
WINDY_API_KEY = "Q2V4GyCCzdkfMxBXqrplP2UbxXLjBrEn"
water_quality_stations_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E5%9F%9F%E6%B0%B4%E8%B3%AA%E6%B8%AC%E7%AB%99.geojson"

# 天氣與潮汐預報 JSON URL
weather_forecast_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E8%B1%A1%E8%B3%87%E6%96%99%E9%A0%90%E5%A0%B1.json"
tide_forecast_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%BD%AE%E6%B1%90%E9%A0%90%E5%A0%B1-%E6%9C%AA%E4%BE%861%E5%80%8B%E6%9C%88%E6%BD%AE%E6%B1%90%E9%A0%90%E5%A0%B1.json"

# Streamlit 應用標題
st.title("Windy與氣象資料預測")

# 設定地圖的初始中心位置與縮放級別
initial_lat, initial_lon = 23.5, 121  # 台灣中間位置
zoom_level = 6

# 初始化 session_state
if "windy_lat" not in st.session_state:
    st.session_state["windy_lat"] = initial_lat
    st.session_state["windy_lon"] = initial_lon
    st.session_state["windy_zoom"] = zoom_level

# 左側：Windy 動態風速圖
st.write("### Windy 動態風速")
windy_url = f"""
<iframe 
    width="100%" 
    height="500" 
    src="https://embed.windy.com/embed2.html?lat={st.session_state['windy_lat']}&lon={st.session_state['windy_lon']}&zoom={st.session_state['windy_zoom']}&level=surface&overlay=wind&menu=&message=&marker=&calendar=&pressure=&type=map&location=coordinates&detail=&detailLat={st.session_state['windy_lat']}&detailLon={st.session_state['windy_lon']}&metricWind=default&metricTemp=default&radarRange=-1&key={WINDY_API_KEY}" 
    frameborder="0">
</iframe>
"""
st.components.v1.html(windy_url, height=500)

# 右側：水質測站點位地圖
st.write("### 水質測站點位")
m = leafmap.Map(center=[st.session_state["windy_lat"], st.session_state["windy_lon"]], zoom=zoom_level)
m.add_basemap("OpenStreetMap")
m.add_geojson(water_quality_stations_url, layer_name="水質測站點位")

# 處理點擊事件
click_info = st_folium(m, width=700, height=500)

# 偵測點擊並更新 Windy iframe
if click_info and click_info.get("last_clicked"):
    clicked_lat = click_info["last_clicked"]["lat"]
    clicked_lon = click_info["last_clicked"]["lng"]
    st.session_state["windy_lat"] = clicked_lat
    st.session_state["windy_lon"] = clicked_lon
    st.session_state["windy_zoom"] = 12
    st.experimental_rerun()

# 下方：氣象與潮汐預報
st.write("### 台灣周遭海域海象預測(6hr)")

# 解析天氣與潮汐預報 JSON 資料
try:
    # 天氣預報處理
    weather_data = pd.read_json(weather_forecast_url)
    location_data = weather_data["cwaopendata"]["dataset"]["location"]

    # 天氣資料表
    weather_table = []
    for location in location_data:
        loc_name = location["locationName"]
        for element in location["weatherElement"]:
            for time_data in element["time"]:
                weather_table.append({
                    "地點": loc_name,
                    "要素": element["elementName"],
                    "起始時間": time_data["startTime"],
                    "結束時間": time_data["endTime"],
                    "描述": time_data["parameter"]["parameterName"],
                    "數值": time_data["parameter"].get("parameterValue", "N/A")
                })
    weather_df = pd.DataFrame(weather_table)
    st.dataframe(weather_df)

    # 潮汐預報處理
    tide_data = pd.read_json(tide_forecast_url)
    tide_forecasts = tide_data["cwaopendata"]["Resources"]["Resource"]["Data"]["TideForecasts"]

    # 潮汐資料表
    tide_table = []
    for forecast in tide_forecasts:
        loc_name = forecast["Location"]["LocationName"]
        daily_data = forecast["Location"]["TimePeriods"]["Daily"]
        for day in daily_data:
            for tide in day["Time"]:
                tide_table.append({
                    "地點": loc_name,
                    "日期": day["Date"],
                    "潮汐": tide["Tide"],
                    "潮高 (AboveTWVD)": tide["TideHeights"]["AboveTWVD"],
                    "時間": tide["DateTime"]
                })
    tide_df = pd.DataFrame(tide_table)
    st.write("### 潮汐預報")
    st.dataframe(tide_df)

except Exception as e:
    st.error(f"無法載入或解析 JSON 資料: {e}")
