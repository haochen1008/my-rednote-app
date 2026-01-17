import streamlit as st
st.title("🏠 GitHub 迁移成功！")
st.write("如果你看到这个，说明 Streamlit Cloud 已经接通了。")
text = st.text_area("粘贴 Rightmove 描述：")
if st.button("模拟转换"):
    st.balloons()
    st.success("准备接入 AI...")
