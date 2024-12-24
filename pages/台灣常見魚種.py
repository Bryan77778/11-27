import streamlit as st

# 圖片網址
image_urls = [
    "https://i.imgur.com/dwcaKvQ.jpeg",
    "https://i.imgur.com/VlARaQ4.jpeg"
]

# 創建分頁
tabs = st.tabs(["Image 1", "Image 2"])

# 在每個分頁中顯示圖片
for tab, image_url in zip(tabs, image_urls):
    with tab:
        st.image(image_url, caption=image_url, use_column_width=True)
