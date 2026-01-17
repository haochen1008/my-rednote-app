import streamlit as st
import requests
from bs4 import BeautifulSoup
import json

st.set_page_config(page_title="Rightmove 全能助手", page_icon="🏠")

# 你的 API 信息
API_KEY = "sk-d99a91f22bf340139a335fb3d50d0ef5"

def get_rightmove_info(url):
    # 模拟真实浏览器，防止白屏被封
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 尝试抓取标题和描述
            title = soup.title.string if soup.title else "未找到标题"
            # Rightmove 描述的常用标签
            desc_div = soup.find('div', {'class': 're-feeds-description'}) or soup.find('div', {'itemprop': 'description'})
            content = desc_div.get_text(separator="\n") if desc_div else "未抓取到正文，请手动检查链接。"
            return title, content
        else:
            return "访问受限", f"错误码：{response.status_code}。Rightmove 暂时屏蔽了自动抓取。"
    except Exception as e:
        return "抓取失败", str(e)

st.title("🏠 Rightmove 一键搬运")

url = st.text_input("第一步：粘贴 Rightmove 链接", placeholder="https://www.rightmove.co.uk/properties/...")

if st.button("🔍 提取信息"):
    if url:
        with st.spinner('正在破解 Rightmove 保护并提取数据...'):
            title, content = get_rightmove_info(url)
            st.subheader(f"📍 {title}")
            # 把抓到的内容自动放进文本框，方便 AI 处理
            st.session_state['desc_content'] = content
            st.success("提取成功！")
    else:
        st.error("请输入链接")

# 如果提取到了内容，或者用户想手动输入
desc_to_process = st.text_area("第二步：确认描述内容", value=st.session_state.get('desc_content', ''), height=200)

if st.button("🚀 生成小红书爆款文案"):
    if desc_to_process:
        with st.spinner('AI 正在转换文案...'):
            # 这里调用 DeepSeek 逻辑 (代码同前，建议充值 2 元后再试)
            st.balloons()
