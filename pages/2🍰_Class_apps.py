import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import qrcode
from PIL import Image
from wordcloud import WordCloud
import streamlit.components.v1 as components  # For embedding YouTube videos / iframe
from gtts import gTTS
import io
from streamlit_drawable_canvas import st_canvas
import random

# Function to create word cloud
def create_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud

# Streamlit tabs (✅ WordCloud tab inserted as 4th)
tabs = st.tabs([
    "✏️Blackboard", "📈QR", "⏳Timer",
    "☁️WordCloud",           # ✅ NEW 4th tab
    "🐤GS", "🔊TTS", "🎨Drawing", "👥Grouping",
])

# --- Tab 0: Blackboard ---
with tabs[0]:
    st.subheader("📚 Blackboard")

    c1, c2 = st.columns([1, 1])
    with c1:
        font_size = st.slider("Text size", 12, 124, 32, 2)
    with c2:
        text_color = st.color_picker("Text color", "#ffffff")

    text = st.text_area("✍️ Write on the board", height=100, placeholder="Type your ideas here...")

    st.markdown(
        f"""
        <div style="
            background-color: #006666;
            padding: 1.5rem;
            border-radius: 10px;
            min-height: 250px;
            font-size: {font_size}px;
            color: {text_color};
            line-height: 1.6;
            white-space: pre-wrap;
        ">
        {text if text.strip() else " "}
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- Tab 1: QR ---
with tabs[1]:
    st.caption("QR code generator")

    col1, col2, col3 = st.columns([3, 3, 2])
    with col1:
        qr_link = st.text_input("📌 Enter URL link:", key="qr_link")
    with col2:
        caption = st.text_input("Enter a caption (optional):", key="qr_caption")
    with col3:
        st.write("")
        generate_qr_button = st.button("🔆 Click to Generate QR", key="generate_qr")

    if generate_qr_button and qr_link:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_link)
        qr.make(fit=True)

        qr_img = qr.make_image(fill='black', back_color='white').convert('RGB').resize((600, 600))
        st.image(qr_img, caption=caption if caption else "Generate", use_container_width=False, width=400)

# --- Tab 2: Timer ---
with tabs[2]:
    huggingface_space_url = "https://MK-316-mytimer.hf.space"
    st.components.v1.html(
        f"""
        <iframe src="{huggingface_space_url}" width="100%" height="600px" frameborder="0"
                allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen></iframe>
        """,
        height=600
    )

# --- Tab 3: ✅ NEW WordCloud ---
with tabs[3]:
    st.subheader("☁️ WordCloud Generator")
    st.caption("Paste text below and generate a word cloud.")

    wc_text = st.text_area(
        "📋 Paste text here",
        height=220,
        placeholder="Paste your text here...",
        key="wc_text"
    )

    # Optional controls (safe defaults)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        max_words = st.slider("Max words", 30, 300, 120, 10)
    with c2:
        bg = st.selectbox("Background", ["white", "black"], index=0)
    with c3:
        colormap = st.selectbox("Color style", ["viridis", "plasma", "inferno", "magma", "cividis"], index=0)

    if st.button("✨ Generate WordCloud", key="btn_wc"):
        if not wc_text.strip():
            st.warning("Please paste some text first.")
        else:
            wc = WordCloud(
                width=1000,
                height=500,
                background_color=bg,
                max_words=max_words,
                colormap=colormap
            ).generate(wc_text)

            fig, ax = plt.subplots(figsize=(12, 6))
            ax.imshow(wc, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)

# --- Tab 4: (was tabs[3]) Google Sheet ---
with tabs[4]:
    st.markdown("#### Google Sheet to share for Class Activities")
    st.markdown("""
    + Working group (1st week)
    """)
    st.markdown("---")

    button_html = """
        <style>
            .custom-button {
                background-color: #003366;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
            }
            .custom-button:hover {
                background-color: #002244;
            }
        </style>
        <a href="https://docs.google.com/spreadsheets/d/1JsW8sRnnVAMwgUSpXK3ygO0YvJqzLC5ZucOF_523Lzg/edit?usp=sharing" target="_blank">
            <button class="custom-button">🎯 Click: Go to Google Sheet</button>
        </a>
    """
    st.markdown(button_html, unsafe_allow_html=True)

# --- Tab 5: (was tabs[4]) TTS ---
with tabs[5]:
    st.subheader("Text-to-Speech Converter (using Google TTS)")
    text_input = st.text_area("Enter the text you want to convert to speech:")
    language = st.selectbox(
        "Choose a language: 🇰🇷 🇺🇸 🇬🇧 🇷🇺 🇫🇷 🇪🇸 🇯🇵 ",
        ["Korean", "English (American)", "English (British)", "Russian", "Spanish", "French", "Japanese"]
    )

    tts_button = st.button("Convert Text to Speech")
    if tts_button and text_input:
        lang_codes = {
            "Korean": ("ko", None),
            "English (American)": ("en", 'com'),
            "English (British)": ("en", 'co.uk'),
            "Russian": ("ru", None),
            "Spanish": ("es", None),
            "French": ("fr", None),
            "Chinese": ("zh-CN", None),
            "Japanese": ("ja", None)
        }
        language_code, tld = lang_codes[language]

        if tld:
            tts = gTTS(text=text_input, lang=language_code, tld=tld, slow=False)
        else:
            tts = gTTS(text=text_input, lang=language_code, slow=False)

        speech = io.BytesIO()
        tts.write_to_fp(speech)
        speech.seek(0)
        st.audio(speech.getvalue(), format='audio/mp3')

    st.markdown("---")
    st.caption("🇺🇸 English text: Teacher-designed coding applications create tailored learning experiences, making complex concepts easier to understand through interactive and adaptive tools. They enhance engagement, provide immediate feedback, and support active learning.")
    st.caption("🇰🇷 Korean text: 교사가 직접 만든 코딩 기반 애플리케이션은 학습자의 필요에 맞춘 학습 경험을 제공하고, 복잡한 개념을 쉽게 이해하도록 돕습니다. 또한 학습 몰입도를 높이고 즉각적인 피드백을 제공하며, 능동적인 학습을 지원합니다.")
    st.caption("🇫🇷 French: Les applications de codage conçues par les enseignants offrent une expérience d'apprentissage personnalisée, rendant les concepts complexes plus faciles à comprendre grâce à des outils interactifs et adaptatifs. Elles améliorent l'engagement, fournissent un retour immédiat et soutiennent l'apprentissage actif.")
    st.caption("🇷🇺 Russian: Созданные учителями кодированные приложения предлагают персонализированный опыт обучения, упрощая понимание сложных концепций с помощью интерактивных и адаптивных инструментов. Они повышают вовлеченность, предоставляют мгновенную обратную связь и поддерживают активное обучение.")
    st.caption("🇨🇳 Chinese: 由教师设计的编程应用程序为学习者提供个性化的学习体验，通过互动和适应性工具使复杂的概念更容易理解。它们增强学习参与度，提供即时反馈，并支持主动学习。")
    st.caption("🇯🇵 Japanese: 教師が設計したコーディングアプリケーションは、学習者のニーズに合わせた学習体験を提供し、複雑な概念をインタラクティブで適応性のあるツールを通じて理解しやすくします。また、学習への集中力を高め、即時フィードバックを提供し、主体的な学習をサポートします。")

# --- Tab 6: (was tabs[5]) Drawing ---
with tabs[6]:
    st.caption("Use the canvas below to draw freely. You can change the stroke width and color.")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        stroke_width = st.slider("✏️ Stroke Width", 1, 10, 5)
    with col2:
        stroke_color = st.color_picker("🖌 Stroke Color", "#000000")
    with col3:
        bg_color = st.color_picker("🖼 Background Color", "#FFFFFF")

    if "clear_canvas" not in st.session_state:
        st.session_state["clear_canvas"] = False

    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=400,
        width=600,
        drawing_mode="freedraw",
        key="main_canvas" if not st.session_state["clear_canvas"] else "new_canvas"
    )

    if st.button("🗑️ Clear Canvas"):
        st.session_state["clear_canvas"] = not st.session_state["clear_canvas"]
        st.rerun()

# --- Tab 7: (was tabs[6]) Grouping ---
with tabs[7]:
    st.subheader("👥 Grouping Tool")
    st.caption("Your CSV should have at least the columns `Course` and `Name_ori`.")

    default_url = "https://raw.githubusercontent.com/MK316/english-phonetics/refs/heads/main/pages/data/F25-roster-total-0901.csv"
    uploaded_file = st.file_uploader("🌱 Step1: Upload your CSV file (optional)", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        source_label = "✅ File uploaded"
    else:
        df = pd.read_csv(default_url)
        source_label = "📂 Using default GitHub data"

    if all(col in df.columns for col in ['Course', 'Name_ori']):
        st.success(source_label)

        course_list = df['Course'].dropna().unique().tolist()
        selected_course = st.selectbox("🌱 Step 2: Select Course for Grouping", course_list)

        st.markdown("##### 🌱 Step3: Group Settings (Currently 17 students: 3*3G and 4*2G)")
        num_group3 = st.number_input("Number of 3-member groups", min_value=0, step=1)
        num_group4 = st.number_input("Number of 4-member groups", min_value=0, step=1)

        if st.button("🌱 Step 4: Generate Groups"):
            course_df = df[df['Course'] == selected_course]
            names = course_df['Name_ori'].dropna().tolist()
            random.shuffle(names)

            total_needed = num_group3 * 3 + num_group4 * 4
            if total_needed > len(names):
                st.error(f"❗ Not enough students in {selected_course}. Requested {total_needed}, available {len(names)}.")
            else:
                grouped_data = []
                group_num = 1

                for _ in range(num_group3):
                    members = names[:3]
                    names = names[3:]
                    grouped_data.append([f"Group {group_num}"] + members)
                    group_num += 1

                for _ in range(num_group4):
                    members = names[:4]
                    names = names[4:]
                    grouped_data.append([f"Group {group_num}"] + members)
                    group_num += 1

                max_members = max(len(group) - 1 for group in grouped_data)
                columns = ['Group'] + [f'Member{i+1}' for i in range(max_members)]
                grouped_df = pd.DataFrame(grouped_data, columns=columns)

                st.success(f"✅ {selected_course}: Grouping complete!")
                st.write(grouped_df)

                csv_buffer = io.StringIO()
                grouped_df.to_csv(csv_buffer, index=False)
                st.download_button(
                    label="📥 Download Grouped CSV",
                    data=csv_buffer.getvalue().encode('utf-8'),
                    file_name=f"grouped_{selected_course.replace(' ', '_')}.csv",
                    mime="text/csv"
                )
    else:
        st.error("The file must contain both `Course` and `Name_ori` columns.")
