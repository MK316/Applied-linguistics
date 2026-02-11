import streamlit as st
import requests

tab1, tab2, tab3, tab4 = st.tabs(["🌵 Online platforms", "🌵Vibe coding", "🌵 Github collaboration", "🌵 Python coding"])

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

    **🔹 Python**  
    + Manual online: https://wikidocs.net/5
    + Manual 2: [Coding4ET](https://github.com/MK316/Coding4ET/blob/main/README.md)
    + Basic Python manual in Korean
    
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
    
    st.markdown("""
    + [Understanding Vibe coding](https://github.com/MK316/Applied-linguistics/blob/main/mdfiles/vibe01.md)
    + Online platform: [Cursor](https://cursor.com/), [Replit Agent](https://replit.com/?utm_source=youtube&utm_medium=youtube&utm_campaign=youtube&gad_source=1&gad_campaignid=22257718739&gbraid=0AAAAA-k_HqIrzlum39bUXIpKSBAcWHWFk&gclid=Cj0KCQiA7rDMBhCjARIsAGDBuEBb4hwKyYOy0AlRtuzvp3xYmu2TpMo6Du7M7NhpQvpEIhb0eoRqLwUaAiBYEALw_wcB), GitHub Spark, [Lovable](https://lovable.dev/videos/vibe%20coding)

with tab3:
    st.markdown("📄 Github repository for class collaboration: [link](https://github.com/MK316/Collaboration26/blob/main/README.md)")

    try:
        r = requests.get(README_URL, timeout=10)
        r.raise_for_status()
        st.markdown(r.text)
    except Exception as e:
        st.error(f"Could not load README file.\n{e}")

with tab4:
    st.caption("Python manual for English Teachers (workbook manual)")

    README_URL = "https://raw.githubusercontent.com/MK316/Coding4ET/main/README.md"

    try:
        response = requests.get(README_URL, timeout=10)
        response.raise_for_status()
        st.markdown(response.text)
    except Exception as e:
        st.error(f"Could not load the README file.\n{e}")



