import streamlit as st
import requests
import json

# 1. 基础配置
st.set_page_config(page_title="Rightmove 助手", page_icon="🏠")

API_KEY = "sk-d99a91f22bf340139a335fb3d50d0ef5"
API_URL = "https://api.deepseek.com/chat/completions"

def generate_post(en_desc, style):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    prompt = f"你是一个专业的小红书房产博主。请根据以下Rightmove英文描述写一篇中文爆款文案。风格：{style}。英文内容：{en_desc}"
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}]
    }
    res = requests.post(API_URL, headers=headers, json=data)
    return res.json()['choices'][0]['message']['content']

# 2. 界面设计
st.title("🏠 小红书房产搬运神器")
st.markdown("---")

# 左右分栏
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("第一步：提供素材")
    # 虽然自动抓取受限，但你可以直接把链接里的描述考过来
    desc = st.text_area("粘贴 Rightmove 描述：", height=250, placeholder="将链接里的 Description 复制到这里...")
    
    # 增加图片预览功能
    uploaded_files = st.file_uploader("可选：上传房源照片 (多选)", accept_multiple_files=True)
    if uploaded_files:
        st.write(f"已加载 {len(uploaded_files)} 张照片")

with col2:
    st.subheader("第二步：生成文案")
    style = st.selectbox("文案风格", ["爆款营销", "温馨居家", "专业分析"])
    if st.button("🚀 生成小红书文案"):
        if not desc:
            st.warning("请先粘贴描述内容")
        else:
            with st.spinner('AI 构思中...'):
                try:
                    result = generate_post(desc, style)
                    st.markdown(result)
                    st.balloons()
                except:
                    st.error("余额不足或 Key 无效，请检查 DeepSeek 账户")

if uploaded_files:
    st.write("---")
    st.subheader("🖼️ 图片预览 (可直接右键保存)")
    cols = st.columns(3)
    for idx, file in enumerate(uploaded_files):
        cols[idx % 3].image(file, use_container_width=True)
