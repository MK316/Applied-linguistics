import streamlit as st

st.title("📚 Course Overview")
st.caption("Fun English · Spring 2026")

st.markdown(
    """
    <div style="
        background-color: #f8fbff;
        border: 2px solid #dfe8ff;
        border-radius: 22px;
        padding: 28px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        margin-bottom: 20px;
    ">
        <div style="font-size: 54px;">🌱📚✨</div>
        <h2 style="color:#1f4e79;">Welcome to Fun English!</h2>
        <p style="font-size:20px;">
            Learn English step by step through words, listening, speaking, reading, and fun activities.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader("✨ Course Menu")

st.markdown(
    """
    - 🔤 **Word Quiz**: Learn basic words with pictures and sounds  
    - ⏳ **Tense Practice**: Practice present, past, future, and present progressive  
    - 📖 **Lecture Slides**: Read short passages and class materials  
    - 🧰 **Class Apps**: Use tools for classroom activities  
    - 👥 **Grouping**: Make groups for pair and team work  
    """
)

st.subheader("🎯 Goal")

st.success("English is not just a subject. It is a tool for communication.")
