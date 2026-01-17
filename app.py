import streamlit as st
import requests
import base64

# 1. 页面配置
st.set_page_config(page_title="房产全能搬运助手", layout="wide")

# 配置你的 DeepSeek Key (建议充值2元后使用)
API_KEY = "sk-d99a91f22bf340139a335fb3d50d0ef5"

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

def process_with_ai(content, mode, platform):
    url = "https://api.deepseek.com/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    # 根据平台调整指令
    prompts = {
        "小红书": "写一篇爆款小红书笔记，多用Emoji，分段清晰，带10个标签，语气要‘家人们谁懂啊’。",
        "朋友圈": "写一段精炼的朋友圈文案，语气专业且亲切，适合私域转化，控制在150字以内。",
        "抖音": "写一段带节奏感的短视频脚本。包含：【画面描述】、【旁白台词】、【热门BGM建议】。"
    }
    
    selected_prompt = prompts.get(platform, "翻译并润色文案")
    
    # 如果是文本模式
    if mode == "text":
        messages = [{"role": "user", "content": f"{selected_prompt}\n内容如下：\n{content}"}]
    # 如果是图片模式 (注意：DeepSeek 目前主模型需要使用 vision 模型才能识图)
    # 这里我们采用通用的多模态逻辑
    else:
        messages = [{
            "role": "user",
            "content": [
                {"type": "text", "text": f"请识别这张截图里的房源描述，并直接按照这个要求生成文案：{selected_prompt}"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{content}"}}
            ]
        }]

    payload = {
        "model": "deepseek-chat", # 提示：DeepSeek 识图建议使用 deepseek-vision 模型
        "messages": messages,
        "max_tokens": 1000
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content']

# 2. 界面设计
st.title("🏠 房产全能搬运助手")
st.markdown("---")

tab1, tab2 = st.tabs(["📸 截图识别", "✍️ 手动粘贴"])

with tab1:
    st.subheader("上传 Rightmove 描述截图")
    img_file = st.file_uploader("支持手机截图或网页长图", type=['png', 'jpg', 'jpeg'])
    if img_file:
        st.image(img_file, width=300, caption="已上传截图")

with tab2:
    st.subheader("手动粘贴文本")
    text_input = st.text_area("在此粘贴 Description...", height=200)

st.markdown("---")
st.subheader("选择发布平台")
platform = st.segmented_control("发布到：", ["小红书", "朋友圈", "抖音"], default="小红书")

if st.button("🚀 开始魔法转换"):
    with st.spinner('AI 正在全力处理中...'):
        try:
            if img_file: # 图片模式
                base64_img = encode_image(img_file)
                result = process_with_ai(base64_img, "image", platform)
            elif text_input: # 文本模式
                result = process_with_ai(text_input, "text", platform)
            else:
                st.warning("请先上传图片或输入文字内容")
                st.stop()
            
            st.success(f"✨ {platform} 版本已生成！")
            st.markdown(result)
            st.balloons()
        except Exception as e:
            st.error(f"生成失败：请检查 DeepSeek 余额或 Key 是否正确。")
