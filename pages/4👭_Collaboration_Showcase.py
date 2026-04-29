import streamlit as st
import requests

st.set_page_config(page_title="Learning Tools", layout="wide")

st.caption("Making learning tools and share codes")

tab1, tab2, tab3 = st.tabs([
    "1. mini project",
    "2. APP showcase (selected)",
    "3. Final Project: Lesson plan"
])

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

    PROJECTS = {
        "Select a project": None,
        "Overview & guidelines": "https://raw.githubusercontent.com/MK316/Collaboration26/main/mini-project/readme.md",
        "Sample - Multi-language TTS": "https://raw.githubusercontent.com/MK316/Collaboration26/main/mini-project/sample.md",
        "🍩 Project 1 - Sentence by Sentence TTS": "https://github.com/MK316/Collaboration26/raw/main/mini-project/miniproject-sample.md",
        "🍩 Project 2 - Verb Learning": "https://github.com/JHC0531/Mini-project/raw/main/README.md",
        "🍩 Project 3 - Project title": "https://github.com/kwonsungja/MiniProject/raw/main/README.md",
        "Giving Feedback": "https://forms.gle/1rDSAf8q8HexoVg78"
    }

    selected_project = st.selectbox(
        "Choose a mini project",
        options=list(PROJECTS.keys()),
        index=0,
        key="mini_project_select"
    )

    md_url = PROJECTS[selected_project]

    if md_url:
        if selected_project == "Giving Feedback":
            st.markdown("### Giving Feedback")
            st.write("Click the button below to open the peer feedback form.")
            st.link_button("Open Feedback Form", md_url)
        else:
            st.markdown("### Project overview")
            md_text = load_markdown_from_url(md_url)
            st.markdown(md_text)

            st.divider()
            st.caption("The markdown file above can include the app link.")


with tab2:
    st.write("Collaboration apps will be displayed here in time.")


with tab3:
    st.write("Final project: 50-minute lesson plan with a customized app.")

    FINAL_PROJECTS = {
        "Select a final project": None,
        "Overview & guidelines": "https://github.com/MK316/Collaboration26/raw/main/final-project/README.md",
        "Sample final project": "https://raw.githubusercontent.com/MK316/Collaboration26/main/final-project/sample.md",
        "Project 1": "https://raw.githubusercontent.com/USERNAME/REPO/main/README.md",
        "Project 2": "https://raw.githubusercontent.com/USERNAME/REPO/main/README.md",
        "Project 3": "https://raw.githubusercontent.com/USERNAME/REPO/main/README.md",
        "Project 4": "https://raw.githubusercontent.com/USERNAME/REPO/main/README.md",
        "Project 5": "https://raw.githubusercontent.com/USERNAME/REPO/main/README.md",
        "Project 6": "https://raw.githubusercontent.com/USERNAME/REPO/main/README.md",
        "Project 7": "https://raw.githubusercontent.com/USERNAME/REPO/main/README.md",
        "Giving Feedback": "https://forms.gle/5QLKafV9BxNonms69"
    }

    selected_final_project = st.selectbox(
        "Choose a final project",
        options=list(FINAL_PROJECTS.keys()),
        index=0,
        key="final_project_select"
    )

    final_md_url = FINAL_PROJECTS[selected_final_project]

    if final_md_url:
        if selected_final_project == "Giving Feedback":
            st.markdown("### Giving Feedback")
            st.write("Click the button below to open the final project peer feedback form.")
            st.link_button("Open Feedback Form", final_md_url)
        else:
            st.markdown("### Final project overview")
            final_md_text = load_markdown_from_url(final_md_url)
            st.markdown(final_md_text)

            st.divider()
            st.caption("The markdown file above can include the lesson plan and app link.")
