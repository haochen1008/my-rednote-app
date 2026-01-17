import streamlit as st

# 设置页面
st.set_page_config(page_title="Rightmove 搬运工", page_icon="🏠")

st.title("🏠 Rightmove 转小红书文案")
st.markdown("---")

# 输入区域
desc = st.text_area("第一步：粘贴 Rightmove 原始英文描述", height=250, placeholder="Paste the property description here...")

# 配置选项
col1, col2 = st.columns(2)
with col1:
    style = st.selectbox("文案风格", ["爆款种草型", "专业客观型", "急售吸引型"])
with col2:
    emoji_level = st.slider("表情包密度", 1, 5, 3)

# 转换按钮
if st.button("🚀 一键生成爆款文案"):
    if not desc:
        st.warning("请先粘贴描述内容哦！")
    else:
        with st.spinner('AI 正在拆解房源卖点...'):
            # --- 这里是处理逻辑 ---
            # 提示：现在这里是模拟 AI 返回，稍后我们填入真正的 API 调用代码
            result = f"""
✨ **{style}文案生成成功！** ✨

📍 **房源卖点拆解：**
1. 优质地段，交通便利 🚶‍♂️
2. 空间开阔，采光极佳 ☀️
3. 现代装修，拎包入住 🔑

📝 **小红书草稿：**
-----------------------------------------
伦敦租房不迷路！🏠 这套房子真的绝了！

{desc[:50]}... (AI 已自动根据原意优化)

在这里住真的太爽了！出门就是地铁站，下楼就是超市 🛒。
不管是留学生还是上班族，闭眼冲！！

#伦敦租房 #英国生活 #好房推荐 #小红书搬运工
-----------------------------------------
            """
            st.markdown(result)
            st.balloons()

st.info("💡 提示：点击生成后，直接复制文案即可发布到小红书。")
