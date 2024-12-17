import streamlit as st

# Streamlit 應用標題
st.title("Windy API Map Forecast Viewer")

# 固定的 API Key 和應用網址
api_key = "Q2V4GyCCzdkfMxBXqrplP2UbxXLjBrEn"
base_url = "https://homepy-nucjfvrzwsjfmngjr2xgsr.streamlit.app"

# Windy 地圖嵌入設定
st.write("以下是透過 Windy API 顯示的天氣預報地圖：")

# 直接嵌入 Windy 地圖（不需要額外輸入 API Key）
windy_embed_code = f"""
<iframe 
    width="800" 
    height="600" 
    src="https://embed.windy.com/embed2.html?lat=25&lon=121&zoom=5&level=surface&overlay=wind&menu=&message=&marker=&calendar=&pressure=&type=map&location=coordinates&detail=&detailLat=25&detailLon=121&metricWind=default&metricTemp=default&radarRange=-1&key={api_key}" 
    frameborder="0">
</iframe>
"""

# 使用 Streamlit 顯示地圖
st.components.v1.html(windy_embed_code, height=600)
    st.error(f"發生錯誤: {e}")
