import streamlit as st

# Streamlit 應用標題
st.title("Windy API Map Forecast Viewer")

# 輸入 API Key 和其他設定
api_key = st.text_input("請輸入您的 Windy API Key", type="password")
st.write("請將此網頁應用於您指定的網域，並確保 API Key 正確。")

# 嵌入 Windy 地圖（需要 Windy API Key）
if api_key:
    windy_embed_code = f"""
    <iframe 
        width="800" 
        height="600" 
        src="https://embed.windy.com/embed2.html?lat=25&lon=121&zoom=5&level=surface&overlay=wind&menu=&message=&marker=&calendar=&pressure=&type=map&location=coordinates&detail=&detailLat=25&detailLon=121&metricWind=default&metricTemp=default&radarRange=-1" 
        frameborder="0">
    </iframe>
    """
    st.components.v1.html(windy_embed_code, height=600)
else:
    st.warning("請輸入有效的 Windy API Key 才能顯示地圖。")
