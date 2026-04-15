import streamlit as st
import requests

st.set_page_config(page_title="Learning Tools", layout="wide")

st.caption("Making learning tools and share codes")

tab1, tab2, tab3 = st.tabs(["1. mini project", "2. Focus apps", "3. Lesson plan"])

# -----------------------------
# Helper: GitHub raw markdown load
# -----------------------------
def load_markdown_from_url(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.text
    except requests.exceptions.RequestException as e:
        return f"Failed to load markdown file.\n\n{e}"

with tab1:
    st.write("Mini project in pairs.")

    # 학생 프로젝트 4개 틀
    # 아래 url 부분에 실제 GitHub raw md 주소를 넣으면 됨
    PROJECTS = {
        "Select a project": None,
        "Overview & guidelines": "https://raw.githubusercontent.com/MK316/Collaboration26/main/mini-project/readme.md",
        "Sample - Multi-language TTS": "https://raw.githubusercontent.com/MK316/Collaboration26/main/mini-project/sample.md",
        "Pair 1 - Project title": "https://raw.githubusercontent.com/USERNAME/REPO/main/project2.md",
        "Pair 2 - Project title": "https://raw.githubusercontent.com/USERNAME/REPO/main/project3.md",
        "Pair 3 - Project title": "https://raw.githubusercontent.com/USERNAME/REPO/main/project4.md",
    }

    selected_project = st.selectbox(
        "Choose a mini project",
        options=list(PROJECTS.keys()),
        index=0
    )

    md_url = PROJECTS[selected_project]

    if md_url:
        st.markdown("### Project overview")
        md_text = load_markdown_from_url(md_url)
        st.markdown(md_text)

        st.divider()
        st.caption("The markdown file above can include the app link.")

with tab2:
    st.write("Collaboration apps will be displayed here in time.")

with tab3:
    st.write("Collaboration apps will be displayed here in time.")
