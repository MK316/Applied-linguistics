import streamlit as st
import base64
from pathlib import Path

st.set_page_config(layout="wide")

tab1, tab2, tab3 = st.tabs(["Course Overview", "Online Links", "TBA"])

with tab1:
    st.markdown("### 📄 Course Overview (PDF)")

    pdf_path = Path("https://raw.githubusercontent.com/MK316/Applied-linguistics/main/data/S26-appling.pdf")  # ← PDF 파일 경로
    pdf_bytes = pdf_path.read_bytes()
    b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

    st.markdown(
        f"""
        <iframe
            src="data:application/pdf;base64,{b64_pdf}"
            width="100%"
            height="900"
            style="border: none;"
        ></iframe>
        """,
        unsafe_allow_html=True,
    )

with tab2:
    st.write("여기는 탭 2입니다.")

with tab3:
    st.write("여기는 탭 3입니다.")
