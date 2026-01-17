import streamlit as st
import requests

st.set_page_config(page_title="房产搬运全能王", layout="wide")

API_KEY = "sk-d99a91f22bf340139a335fb3d50d0ef5"
API_URL = "https://api.deepseek.com/chat/completions"

def generate_full_content(text, platform, style):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    # 构建超级 Prompt
    prompt = f"""
    你是一个深耕英国房产的自媒体专家。请根据以下内容生成{platform}文案。
    风格偏好：{style}
    
    要求：
    1. 生成3个候选标题：[精确信息型]、[情绪吸引型]、[留学生专用型]。
    2. 提取并生成5-8个热门话题Tag。
    3. 文案内容要精准提取卖点：交通、周边、内部装修。
    4. 自动换算周租金(如果是月租除以4.33)。
    
    原文内容：
    {text}
    """
    
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.8
    }
    
    res = requests.post(API_URL, headers=headers, json=payload)
    return res.json()['choices'][0]['message']['content']

st.title("🏙️ 房产搬运全能王")

# 第一步：输入
desc_input = st.text_area("第一步：粘贴 Rightmove 描述", height=200, placeholder="粘贴 Description...")

# 第二步：选择
col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox("发布平台", ["小红书", "朋友圈", "抖音脚本"])
with col2:
    style = st.selectbox("侧重风格", ["吸引眼球", "专业严谨", "温馨生活"])

# 第三步：生成
if st.button("🚀 一键生成全套内容"):
    if not desc_input:
        st.warning("请先粘贴描述内容")
    else:
        with st.spinner('AI 正在为您定制全套文案...'):
            try:
                result = generate_full_content(desc_input, platform, style)
                st.success("生成完毕！")
                
                # 分开展示结果
                st.markdown("### ✨ 生成结果")
                st.write(result)
                
                st.info("💡 小贴士：你可以直接复制以上内容到笔记应用中。")
                st.balloons()
            except:
                st.error("生成失败，请确认 DeepSeek 余额或网络连接。")

st.markdown("---")
st.caption("建议：手动粘贴描述文字最省钱，识图功能仅在无法复制时使用。")
