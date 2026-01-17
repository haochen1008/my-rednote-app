import streamlit as st
import requests
import re

st.set_page_config(page_title="Hao Harbour", layout="wide")

API_KEY = "sk-d99a91f22bf340139a335fb3d50d0ef5"
API_URL = "https://api.deepseek.com/chat/completions"

def generate_pro_content(text, platform, style):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    prompt = f"""
    你是一个深耕英国房产的营销专家。请根据以下内容生成{platform}文案。
    侧重风格：{style}
    
    【格式要求 - 非常重要】：
    1. 标题部分：生成3个候选标题，每个标题严格限制在20个字符以内（含Emoji）。请用“标题1：”、“标题2：”、“标题3：”作为开头。
    2. 文案主体部分：请直接开始写文案内容。
       - 第一部分是简单明了的要点。
       - 第二部分是带感的内容描述。
       - 第三部分是Tag标签。
    注意：在文案主体中，禁止出现“[简单明了版]”、“[详细种草版]”或“文案主体：”等任何解释性字眼。
    
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

st.title("🏙️ Hao Harbour")

# 输入
desc_input = st.text_area("粘贴 Description", height=150)

col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox("发布平台", ["小红书", "朋友圈", "抖音脚本"])
with col2:
    style = st.selectbox("文案调性", ["⚡️ 简单明了", "🔥 爆款吸睛", "🏠 温馨种草", "📊 专业客观"])

if st.button("🚀 瞬间生成"):
    if not desc_input:
        st.warning("请先粘贴内容")
    else:
        with st.spinner('正在生成...'):
            try:
                raw_result = generate_pro_content(desc_input, platform, style)
                
                # 解析标题和主体
                lines = raw_result.split('\n')
                titles = []
                body_content = []
                
                for line in lines:
                    if re.match(r'标题\d：', line):
                        titles.append(re.sub(r'标题\d：', '', line).strip())
                    else:
                        body_content.append(line)
                
                main_body = "\n".join(body_content).strip()

                st.markdown("---")
                
                # --- 标题展示区 ---
                st.subheader("📌 第一步：选择标题")
                t_cols = st.columns(3)
                for i, t in enumerate(titles[:3]):
                    with t_cols[i]:
                        st.write(f"标题 {i+1}")
                        st.code(t, language="text") # st.code自带复制按钮
                
                # --- 主体展示区 ---
                st.subheader("📝 第二步：文案主体 + Tag")
                st.info("文案已自动去除提示字眼，点击右侧按钮直接复制全文")
                st.code(main_body, language="text")
                
                st.balloons()
            except Exception as e:
                st.error("生成失败，请检查余额。")

# 样式美化
st.markdown("""
<style>
    .stCodeBlock { border-radius: 8px; }
    div[data-testid="stExpander"] { border: none; }
</style>
""", unsafe_allow_html=True)
