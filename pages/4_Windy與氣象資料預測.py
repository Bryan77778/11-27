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
fishweather= "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%B5%B7%E8%B1%A1%E6%95%B8%E5%80%BC%E6%A8%A1%E5%BC%8F%E9%A0%90%E5%A0%B1%E8%B3%87%E6%96%99-%E7%94%9F%E6%B4%BB%E6%B0%A3%E8%B1%A1-%E6%B5%B7%E6%B0%B4%E6%B5%B4%E5%A0%B4%E3%80%81%E4%BC%91%E9%96%92%E6%BC%81%E6%B8%AF%E3%80%81%E6%B5%B7%E9%87%A3%E4%B9%8B%E6%B3%A2%E6%B5%81%E6%A8%A1%E5%BC%8F%E9%A0%90%E5%A0%B1%E8%B3%87%E6%96%99.json"

# Streamlit 應用標題
st.title("Windy與氣象資料預測")
st.markdown(
    """
    <style>
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
                          url('https://i.imgur.com/D6zbNRN.png'); /* 添加半透明黑色遮罩 */
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
    - 選擇不同的Windy圖台，像是風速、溫度、降雨等
    - 可以在Windy內查看未來五天的預測情況
    - 點擊水質測站點位地圖(請勿點到圖標)，Windy圖台會自動更新位置
    - 在下方海象、潮汐預測屬性資料表內搜尋地點，以查看預報
    </div>
    """,
    unsafe_allow_html=True
)

# 設定地圖的初始中心位置與縮放級別
initial_lat, initial_lon = 23.5, 121  # 台灣中間位置
zoom_level = 6

# 初始化 session_state
if "windy_lat" not in st.session_state:
    st.session_state["windy_lat"] = initial_lat
    st.session_state["windy_lon"] = initial_lon
    st.session_state["windy_zoom"] = zoom_level

# 左側：Windy 動態風速圖
st.write("### Windy 動態圖台")
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
st.write("### 台灣周遭海域海象預測(2024-12-22 ~ 2024-12-25)")

# 解析 JSON 資料
try:
    # 讀取氣象資料
    weather_data = pd.read_json(fishweather)  # 使用 'fishweather' 變數來讀取資料
    location_data = weather_data["cwaopendata"]["dataset"]["location"]

    # 組織資料表
    table_data = []
    for location in location_data:
        loc_name = location["LocationName"]  # 使用正確的鍵名 "LocationName"
        wave_height = location["SignificantWaveHeight"]
        wave_direction = location["WaveDirectionForecast"]
        wave_period = location["WavePeriod"]
        ocean_current_direction = location["OceanCurrentDirectionForecast"]
        ocean_current_speed = location["OceanCurrentSpeed"]
        datetime = location["DateTime"]
        
        table_data.append({
            "地點": loc_name,
            "浪高": wave_height,
            "浪向": wave_direction,
            "週期": wave_period,
            "流向": ocean_current_direction,
            "流速": ocean_current_speed,
            "時間": datetime
        })
    
    # 創建 DataFrame 並顯示
    df = pd.DataFrame(table_data)
    st.dataframe(df)

except Exception as e:
    st.error(f"無法載入或解析 JSON 資料: {e}")
    
tide_url = "https://github.com/Bryan77778/11-27/raw/refs/heads/main/%E6%BD%AE%E6%B1%90%E9%A0%90%E5%A0%B1-%E6%9C%AA%E4%BE%861%E5%80%8B%E6%9C%88%E6%BD%AE%E6%B1%90%E9%A0%90%E5%A0%B1.json"

try:
    # 下載資料
    response = requests.get(tide_url)
    response.raise_for_status()
    tide_data = response.json()  # 解析為 JSON 格式

    # 獲取必要的資料結構
    cwaopendata = tide_data.get("cwaopendata", {})
    resources = cwaopendata.get("Resources", {})
    resource_data = resources.get("Resource", {})
    tide_forecasts_raw = resource_data.get("Data", {}).get("TideForecasts", None)

    # 如果 TideForecasts 是字串，嘗試解析為 JSON
    if isinstance(tide_forecasts_raw, str):
        try:
            tide_forecasts = json.loads(tide_forecasts_raw)
        except json.JSONDecodeError:
            st.error("TideForecasts 是無法解析的字串資料。")
            tide_forecasts = None
    elif isinstance(tide_forecasts_raw, list):
        tide_forecasts = tide_forecasts_raw  # 如果是列表，直接使用
    else:
        st.warning("TideForecasts 資料為空或型別未知。")
        tide_forecasts = None
    
    # 準備解析資料
    table_data = []
    if tide_forecasts and isinstance(tide_forecasts, list):
        for forecast in tide_forecasts:
            # 確認 Location 是字典
            location = forecast.get("Location", {})
            if not isinstance(location, dict):
                continue

            loc_name = location.get("LocationName", "未知地點")
            latitude = location.get("Latitude", "未知緯度")
            longitude = location.get("Longitude", "未知經度")
            time_periods = location.get("TimePeriods", {})
            daily_data_list = time_periods.get("Daily", [])

            # 確認 Daily 是列表
            if not isinstance(daily_data_list, list):
                continue

            for daily_data in daily_data_list:
                date = daily_data.get("Date", "未知日期")
                lunar_date = daily_data.get("LunarDate", "未知農曆日期")
                tide_range = daily_data.get("TideRange", "未知潮差")
                tide_times = daily_data.get("Time", [])

                # 確認 Time 是列表
                if not isinstance(tide_times, list):
                    continue

                for tide_time in tide_times:
                    # 確認 TideHeights 是字典
                    tide_heights = tide_time.get("TideHeights", {})
                    if not isinstance(tide_heights, dict):
                        tide_heights = {}

                    tide_time_data = {
                        "地點": loc_name,
                        "緯度": latitude,
                        "經度": longitude,
                        "日期": date,
                        "農曆日期": lunar_date,
                        "潮差": tide_range,
                        "潮汐": tide_time.get("Tide", "未知"),
                        "時間": tide_time.get("DateTime", "未知"),
                        "相對台灣高程系統 (cm)": tide_heights.get("AboveTWVD", "N/A"),
                        "相對當地平均海平面 (cm)": tide_heights.get("AboveLocalMSL", "N/A"),
                        "相對海圖 (cm)": tide_heights.get("AboveChartDatum", "N/A"),
                    }
                    table_data.append(tide_time_data)

        # 顯示資料
        if table_data:
            df = pd.DataFrame(table_data)
            st.write("### 潮汐預報資料（近一個月）")
            st.dataframe(df)
        else:
            st.warning("無潮汐資料可供顯示。")
    else:
        st.warning("TideForecasts 資料為空或無法處理。")

except requests.exceptions.RequestException as e:
    st.error(f"無法下載潮汐資料: {e}")
except Exception as e:
    st.error(f"無法處理潮汐資料: {e}")
