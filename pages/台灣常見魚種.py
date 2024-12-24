import streamlit as st

# 標題
st.title("台灣常見魚種")

# 圖片網址
image_urls = [
    "https://i.imgur.com/dwcaKvQ.jpeg",
    "https://i.imgur.com/VlARaQ4.jpeg"
]

# 創建單一分頁
tab = st.tabs(["魚種圖片展示"])[0]

# 在分頁中上下排列顯示圖片
with tab:
    for image_url in image_urls:
        st.image(image_url, caption=image_url, use_container_width=True)
