import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import zipfile
import io

# 配置
st.set_page_config(page_title="Rightmove全能搬运工", layout="wide")
API_KEY = "sk-d99a91f22bf340139a335fb3d50d0ef5"

def fetch_rightmove_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 提取描述 (Rightmove 的描述通常在这个类名下)
        desc_tag = soup.find('div', {'class': 're-feeds-description'}) or soup.find('div', {'itemprop': 'description'})
        description = desc_tag.get_text(separator="\n") if desc_tag else "未能自动抓取到描述，请手动粘贴。"
        
        # 提取图片 (查找所有高清图链接)
        img_tags = soup.find_all('img', {'itemprop': 'contentUrl'})
        images = [img['src'] for img in img_tags if 'src' in img.attrs]
        
        return description, images
    except Exception as e:
        return f"抓取失败: {str(e)}", []

# --- 界面 ---
st.title("🏠 Rightmove 全能搬运助手")
url_input = st.text_input("输入 Rightmove 房源链接：", placeholder="https://www.rightmove.co.uk/properties/...")

if url_input:
    with st.spinner('正在为您提取房源信息...'):
        desc, imgs = fetch_rightmove_data(url_input)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📝 自动提取的描述")
            final_desc = st.text_area("您可以微调描述：", value=desc, height=300)
            
            style = st.select_slider("文案风格", options=["种草型", "专业型", "紧急型"])
            if st.button("🚀 生成小红书文案"):
                # 这里调用你之前的 DeepSeek 逻辑 (generate_rednote_post)
                # ... (为了篇幅，此处省略之前的 AI 函数，逻辑一致)
                st.balloons()
        
        with col2:
            st.subheader("🖼️ 房源图片")
            if imgs:
                st.write(f"共发现 {len(imgs)} 张图片")
                
                # 打包下载逻辑
                buf = io.BytesIO()
                with zipfile.ZipFile(buf, "x") as csv_zip:
                    for i, img_url in enumerate(imgs):
                        img_data = requests.get(img_url).content
                        csv_zip.writestr(f"room_{i}.jpg", img_data)
                
                st.download_button(
                    label="📥 一键打包下载所有图片",
                    data=buf.getvalue(),
                    file_name="house_images.zip",
                    mime="application/zip"
                )
                
                for img in imgs[:5]: # 预览前5张
                    st.image(img, use_column_width=True)
            else:
                st.info("未检测到图片，可能需要手动保存。")
