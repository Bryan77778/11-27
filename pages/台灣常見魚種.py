import streamlit as st

# 標題
st.title("台灣常見魚種")

# 圖片網址
image_urls = [
    "https://github.com/Bryan77778/11-27/blob/main/%E5%8F%B0%E7%81%A3%E5%B8%B8%E8%A6%8B%E9%AD%9A%E7%A8%AE1.jpg?raw=true",
    "https://github.com/Bryan77778/11-27/blob/main/%E5%8F%B0%E7%81%A3%E5%B8%B8%E8%A6%8B%E9%AD%9A%E7%A8%AE2.jpg?raw=true"
]

# 創建單一分頁
tab = st.tabs(["魚種圖片展示"])[0]

# 在分頁中上下排列顯示圖片
with tab:
    for image_url in image_urls:
        st.image(image_url, caption=image_url, use_container_width=True)
