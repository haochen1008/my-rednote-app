import streamlit as st
import requests

st.set_page_config(page_title="Hao Harbour", layout="wide")

API_KEY = "sk-d99a91f22bf340139a335fb3d50d0ef5"
API_URL = "https://api.deepseek.com/chat/completions"

def generate_pro_content(text, platform, style):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    # 核心指令优化：强化“简单明了”逻辑
    prompt = f"""
    你是一个深耕英国房产的营销专家。请根据以下内容生成{platform}文案。
    侧重风格：{style}
    
    【重要指令】：
    1. 标题：生成3个候选标题，每个严格限制在20个字符以内（含Emoji），要吸睛且简短。
    2. 文案结构（请按此顺序排列）：
       - [⚡️ 简单明了版]：必须放在最前面。用极简文字列出：邮编/地段、房型、租金(PW/PCM)、入住时间、周边大学。
       - [✨ 详细种草版]：更具感染力的描述。如果原文内容简陋，请根据地段关键词合理脑补卖点（如周边超市、交通线路、公寓配套）。
    3. 标签：将热门标签（#...）直接放在全文最后。
    4. 标题后面请注明：(复制到小红书标题栏)。
    
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
st.caption("已更新：加入‘简单明了’调性选择 | 标题严格限20字 | 自动补全简陋描述")

# 第一步：输入
desc_input = st.text_area("粘贴 Rightmove 描述（哪怕只有一句话）", height=150, placeholder="Paste description here...")

# 第二步：选择
col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox("发布平台", ["小红书", "朋友圈", "抖音脚本"])
with col2:
    # 这一行已修正，加入了“简单明了”选项
    style = st.selectbox("文案调性", ["⚡️ 简单明了", "🔥 爆款吸睛", "🏠 温馨种草", "📊 专业客观"])

# 第三步：生成
if st.button("🚀 瞬间生成全套文案"):
    if not desc_input:
        st.warning("请先粘贴描述内容哦！")
    else:
        with st.spinner('AI 正在为您定制文案...'):
            try:
                result = generate_pro_content(desc_input, platform, style)
                st.markdown("---")
                st.subheader("📋 文案生成结果")
                
                # 引导语
                st.info("点击下方文本框右上角的图标即可【一键复制全文】")
                
                # 使用 st.code 实现一键复制
                st.code(result, language="markdown")
                
                # 预览区域
                with st.expander("👀 预览文字排版"):
                    st.write(result)
                
                st.balloons()
            except Exception as e:
                st.error("生成出错，可能由于API连接问题或余额波动，请稍后再试。")

# 样式美化
st.markdown("""
<style>
    .stCodeBlock {
        background-color: #f8f9fa !important;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)
