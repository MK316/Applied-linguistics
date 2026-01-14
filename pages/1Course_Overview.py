import streamlit as st
import requests
import base64

tab1, tab2, tab3 = st.tabs(["Course Overview", "Online Links", "TBA"])

@st.cache_data(show_spinner=False)
def load_pdf_bytes(url: str) -> bytes:
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.content

with tab1:
    st.markdown("### 📄 Course Overview (PDF)")

    pdf_url = "https://raw.githubusercontent.com/MK316/Applied-linguistics/main/data/S26-appling.pdf"
    pdf_bytes = load_pdf_bytes(pdf_url)

    b64 = base64.b64encode(pdf_bytes).decode("utf-8")
    pdf_display = f"""
    <iframe
        src="data:application/pdf;base64,{b64}"
        width="100%"
        height="900"
        style="border:none;"
    ></iframe>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)

with tab2:
    st.write("여기는 탭 2입니다.")

with tab3:
    st.write("여기는 탭 3입니다.")
