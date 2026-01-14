import streamlit as st

tab1, tab2, tab3 = st.tabs(["Course Overview", "Online Links", "TBA"])

with tab1:
    st.markdown("### 📄 Course Overview (PDF)")

    pdf_url = "https://raw.githubusercontent.com/MK316/Applied-linguistics/main/data/S26-appling.pdf"

    st.markdown(
        f"""
        <iframe
            src="{pdf_url}"
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
