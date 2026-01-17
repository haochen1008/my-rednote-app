import streamlit as st
import requests
import json

# 1. 基础配置
st.set_page_config(page_title="Rightmove 爆款助手", page_icon="🏠")

# --- 这里是你的 API 配置 ---
API_KEY = "sk-d99a91f22bf340139a335fb3d50d0ef5"
API_URL = "https://api.deepseek.com/chat/completions"

def generate_rednote_post(en_desc, style):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    # AI 角色设定：让它像个专业的小红书房产博主
    prompt = f"""
    你是一个专业的小红书房产博主。请根据以下 Rightmove 的英文描述，写一篇中文小红书文案。
    风格要求：{style}
    
    要求：
    1. 标题要吸引人，包含 Emoji。
    2. 正文分段，列出房源的 3-4 个核心卖点（如交通、装修、采光、周边）。
    3. 语气要亲切、地道，多用小红书常用语（如“家人们”、“谁懂啊”、“神仙房源”）。
    4. 结尾加上 5-8 个相关标签。
    
    英文描述内容：
    {en_desc}
    """
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个精通中英双语的小红书房产营销专家。"},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.text}"

# 2. 界面设计
st.title("🏠 AI 房产搬运工 (DeepSeek 版)")
st.markdown("---")

# 输入框
desc = st.text_area("第一步：粘贴 Rightmove 原始英文描述", height=200, placeholder="Paste the property description here...")

# 选择风格
style = st.select_slider(
    "第二步：选择文案风格",
    options=["极简客观", "温馨种草", "爆款营销", "急售诱人"]
)

# 生成按钮
if st.button("🚀 一键生成爆款文案"):
    if not desc:
        st.warning("请先粘贴描述内容！")
    else:
        with st.spinner('AI 正在读懂你的房子并构思文案...'):
            try:
                result = generate_rednote_post(desc, style)
                st.markdown("### ✨ 生成结果")
                st.write("---")
                st.markdown(result)
                st.balloons()
            except Exception as e:
                st.error(f"出现了一点小问题: {str(e)}")

st.info("💡 提示：生成后如果不满意，可以切换风格再次点击生成。")
