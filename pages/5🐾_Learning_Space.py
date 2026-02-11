import streamlit as st
import requests
import streamlit.components.v1 as components

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📮 Padlet", "🌵 Links", "🌵 Github", "🌵 Vibe coding", "🌵 Collaboration", "🌵 Python", "🌵 Streamlit"])

README_URL = "https://raw.githubusercontent.com/MK316/Collaboration26/main/README.md"

with tab1:
    
    def main():
        st.caption("💙 Class Board: Padlet")
        st.write("➡️ Click the '+' sign to write.")
        # Padlet embed URL (you need to replace this with your actual Padlet embed URL)
        padlet_url = "https://padlet.com/mirankim316/appliedlinguistics"
    
        # Create an iframe to embed the Padlet
        padlet_iframe = f"<iframe src='{padlet_url}' width='100%' height='600' frameborder='0' allow='autoplay'></iframe>"
    
        # Display the iframe in Streamlit
        components.html(padlet_iframe, height=600)
    
    if __name__ == "__main__":
        main()

with tab2:
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

with tab3:
    st.caption("GitHub for Beginners")
    st.markdown("""
    #### Step 1: Introduction to Markdown
    Start with writing rather than coding to lower the barrier to entry.
    
    💧Keywords: .md extension, Headers (#), Lists (*), Links, and Images.
    
    💧Activity: Create a personal profile or a "My Interests" list using Markdown syntax.
    
    ####  Step 2: Understanding Repositories
    Learn the concept of an online "folder" for projects.
    
    💧Keywords: Public vs. Private, README.md, Commit (Saving changes).
    
    💧Activity: Create your first repository (Repo) and upload your Markdown file directly on the GitHub website.
    
     #### Step 3: Collaboration (The Power of Open Source)
    Learn how to contribute to other people's work—the core of GitHub.
    
    💧Keywords: Fork (Copying), Edit, Pull Request (PR) (Requesting to merge changes).
    
    💧Activity: Fork the teacher's repository, add your name to a "Student List," and send a Pull Request.
    
    ####  Step 4: Creating a Streamlit App
    Prepare a simple Python script that will turn into a web page.
    
    💧Keywords: import streamlit as st, st.title(), requirements.txt.
    
    💧Activity: Write a 5-line Python script that displays a welcome message or a simple flashcard.
    
     #### Step 5: Deployment to the Web
    Connect GitHub to Streamlit Cloud to make the app accessible via a URL.
    
    💧Keywords: Streamlit Cloud, Reboot, Live URL.
    
    💧Activity: Link your GitHub repo to Streamlit Cloud, click "Deploy," and share the link with classmates.
    
    ####  Step 6: Maintenance & Continuous Integration
    Understand that software is a living thing that needs updates.
    
    💧Keywords: Live Sync (Auto-update), Debugging, Version History.
    
    💧Activity: Edit the code on GitHub and watch the live website update automatically within seconds.


    """)

with tab4:
    
    st.markdown("""
    + [Understanding Vibe coding](https://github.com/MK316/Applied-linguistics/blob/main/mdfiles/vibe01.md)
    + Online platform: [Cursor](https://cursor.com/), [Replit Agent](https://replit.com/?utm_source=youtube&utm_medium=youtube&utm_campaign=youtube&gad_source=1&gad_campaignid=22257718739&gbraid=0AAAAA-k_HqIrzlum39bUXIpKSBAcWHWFk&gclid=Cj0KCQiA7rDMBhCjARIsAGDBuEBb4hwKyYOy0AlRtuzvp3xYmu2TpMo6Du7M7NhpQvpEIhb0eoRqLwUaAiBYEALw_wcB), GitHub Spark, [Lovable](https://lovable.dev/videos/vibe%20coding).
    """)

with tab5:
    st.markdown("📄 Github repository for class collaboration: [link](https://github.com/MK316/Collaboration26/blob/main/README.md)")

    try:
        r = requests.get(README_URL, timeout=10)
        r.raise_for_status()
        st.markdown(r.text)
    except Exception as e:
        st.error(f"Could not load README file.\n{e}")

with tab6:
    st.caption("Python manual for English Teachers (workbook manual)")

    README_URL = "https://raw.githubusercontent.com/MK316/Coding4ET/main/README.md"

    try:
        response = requests.get(README_URL, timeout=10)
        response.raise_for_status()
        st.markdown(response.text)
    except Exception as e:
        st.error(f"Could not load the README file.\n{e}")


with tab7:
    st.caption("Learn how to deploy your code to build a web application.")
