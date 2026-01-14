import streamlit as st
import streamlit.components.v1 as components

tab1, tab2, tab3 = st.tabs(["Course Overview", "Online Links", "TBA"])

PDF_URL = "https://raw.githubusercontent.com/MK316/Applied-linguistics/main/data/S26-appling.pdf"

with tab1:
    st.markdown("### 📄 Course Overview (PDF)")
    
    # Chrome/Edge에서는 대개 툴바+썸네일 포함 뷰어가 뜹니다.
    iframe_html = f"""
    <iframe
        src="{PDF_URL}#view=FitH"
        width="100%"
        height="900"
        style="border:1px solid #ddd; border-radius:12px;"
    ></iframe>
    """
    components.html(iframe_html, height=920, scrolling=False)
