import streamlit as st
import requests

tab1, tab2, tab3 = st.tabs(["🌵 Online platforms", "🌵 Github collaboration", "🌵 Tab 3"])

README_URL = "https://raw.githubusercontent.com/MK316/Collaboration26/main/README.md"

with tab1:
    st.markdown("### 🌐 Online Platforms & Learning Resources")

    st.markdown("""
    These platforms will be used throughout the course to support coding practice, 
    project collaboration, and the creation of your own digital classroom.

    **🔹 GitHub**  
    + https://github.com
    + File sharing and version control for app code  
    + Collaboration on group projects  
    + Hosting code, data files, and documentation: markdown(e.g., readme.md) file

    **🔹 Google Colab**  
    + https://colab.google/
    + Online Python coding environment (no installation required)  
    + Running and testing code directly in the browser  
    + Useful for beginners practicing Python and data processing

    **🔹 Streamlit**  
    + https://streamlit.io
    + Tool for turning Python scripts into interactive web apps  
    + Used to design and deploy your own class applications  
    + Supports text, audio, charts, quizzes, and learner interaction

    **🔹 Hugging Face**  
    + https://huggingface.co/
    + Online community for AI and language-related tools  
    + Access to pre-trained language and speech models  
    + Exploration of how AI technologies are applied in language learning

    These platforms will help you move from **learning concepts** to **building real educational tools**.
    """)
with tab2:
    st.markdown("📄 Github repository for class collaboration: [link](https://github.com/MK316/Collaboration26/blob/main/README.md)")

    try:
        r = requests.get(README_URL, timeout=10)
        r.raise_for_status()
        st.markdown(r.text)
    except Exception as e:
        st.error(f"Could not load README file.\n{e}")

with tab3:
    st.write("This is Tab 3")


