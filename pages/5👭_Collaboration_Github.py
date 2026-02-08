import streamlit as st


tab1, tab2, tab3 = st.tabs(["Github collaboration", "Tab 2", "Tab 3"])

README_URL = "https://raw.githubusercontent.com/MK316/Collaboration26/main/README.md"

with tab1:
    st.markdown("📄 Github repository for class collaboration: [link](https://github.com/MK316/Collaboration26/blob/main/README.md)")

    try:
        r = requests.get(README_URL, timeout=10)
        r.raise_for_status()
        st.markdown(r.text)
    except Exception as e:
        st.error(f"Could not load README file.\n{e}")

with tab2:
    st.write("This is Tab 2")

with tab3:
    st.write("This is Tab 3")


