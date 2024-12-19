import streamlit as st
import pandas as pd
import json
import leafmap.foliumap as leafmap
from streamlit_folium import st_folium
import requests

# 固定 Windy API Key
WINDY_API_KEY = "Q2V4GyCCzdkfMxBXqrplP2UbxXLjBrEn"
water_quality_stations_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E5%9F%9F%E6%B0%B4%E8%B3%AA%E6%B8%AC%E7%AB%99.geojson"
weather_forecast_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E8%B1%A1%E8%B3%87%E6%96%99%E9%A0%90%E5%A0%B1.json"
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

# 下方：屬性資料表
st.write("### 台灣周遭海域海象預測(6hr)")

# 解析 JSON 資料
try:
    weather_data = pd.read_json(weather_forecast_url)
    location_data = weather_data["cwaopendata"]["dataset"]["location"]

    # 組織資料表
    table_data = []
    for location in location_data:
        loc_name = location["locationName"]
        for element in location["weatherElement"]:
            for time_data in element["time"]:
                table_data.append({
                    "地點": loc_name,
                    "要素": element["elementName"],
                    "起始時間": time_data["startTime"],
                    "結束時間": time_data["endTime"],
                    "描述": time_data["parameter"]["parameterName"],
                    "數值": time_data["parameter"].get("parameterValue", "N/A")
                })
    df = pd.DataFrame(table_data)
    st.dataframe(df)

except Exception as e:
    st.error(f"無法載入或解析 JSON 資料: {e}")

tide_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%BD%AE%E6%B1%90%E9%A0%90%E5%A0%B1-%E6%9C%AA%E4%BE%861%E5%80%8B%E6%9C%88%E6%BD%AE%E6%B1%90%E9%A0%90%E5%A0%B1.json"

st.title("潮汐資料處理")

try:
    # 請求潮汐資料
    response = requests.get(tide_url)
    response.raise_for_status()
    tide_data = response.json()

    # 提取資料結構
    resources = tide_data.get("cwaopendata", {}).get("Resources", {})
    resource_data = resources.get("Resource", {})
    tide_forecasts = resource_data.get("Data", {}).get("TideForecasts", None)

    # 檢查資料型別
    if isinstance(tide_forecasts, str):
        try:
            tide_forecasts = json.loads(tide_forecasts)
        except json.JSONDecodeError:
            st.error("TideForecasts 無法解析為 JSON 格式。")
            tide_forecasts = None

    # 如果 TideForecasts 是列表，繼續處理
    if isinstance(tide_forecasts, list):
        table_data = []
        for forecast in tide_forecasts:
            location = forecast.get("Location", {})
            loc_name = location.get("LocationName", "未知地點")
            latitude = location.get("Latitude", "未知緯度")
            longitude = location.get("Longitude", "未知經度")
            daily_data_list = location.get("TimePeriods", {}).get("Daily", [])

            for daily_data in daily_data_list:
                date = daily_data.get("Date", "未知日期")
                lunar_date = daily_data.get("LunarDate", "未知農曆日期")
                tide_range = daily_data.get("TideRange", "未知潮差")
                tide_times = daily_data.get("Time", [])

                for tide_time in tide_times:
                    table_data.append({
                        "地點": loc_name,
                        "緯度": latitude,
                        "經度": longitude,
                        "日期": date,
                        "農曆日期": lunar_date,
                        "潮差": tide_range,
                        "潮汐": tide_time.get("Tide", "未知"),
                        "時間": tide_time.get("DateTime", "未知"),
                        "相對台灣高程系統 (cm)": tide_time.get("TideHeights", {}).get("AboveTWVD", "N/A"),
                        "相對當地平均海平面 (cm)": tide_time.get("TideHeights", {}).get("AboveLocalMSL", "N/A"),
                        "相對海圖 (cm)": tide_time.get("TideHeights", {}).get("AboveChartDatum", "N/A"),
                    })

        # 建立資料框並顯示
        df = pd.DataFrame(table_data)
        if not df.empty:
            st.write("### 潮汐預報資料")
            st.dataframe(df)
        else:
            st.warning("無潮汐資料可供顯示。")
    else:
        st.error("TideForecasts 資料結構異常，請檢查來源。")

except requests.exceptions.RequestException as e:
    st.error(f"無法下載潮汐資料: {e}")
except Exception as e:
    st.error(f"無法處理潮汐資料: {e}")
