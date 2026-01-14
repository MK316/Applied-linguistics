import streamlit as st

tab1, tab2, tab3 = st.tabs(["Course Overview", "Online Links", "TBA"])

with tab1:
    st.write("여기는 탭 1입니다.")

with tab2:
    st.write("여기는 탭 2입니다.")

with tab3:
    st.write("여기는 탭 3입니다.")
