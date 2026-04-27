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
    "✏️Blackboard", "🎨Drawing", "🔳QR code", "⏳Timer",
    "☁️WordCloud",           # ✅ NEW 4th tab
    "🔊Multi-TTS", "👥Grouping"
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
            min-height: 350px;
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

# ---- Tab2 Drawing
with tabs[1]:
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
        
# --- Tab 3: QR ---
with tabs[2]:
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

# ---


# --- Tab 4: Timer ---
with tabs[3]:
    st.subheader("⏳ Classroom Timer")
    st.caption("Set the time and click Start.")

    col1, col2, col3 = st.columns(3)

    with col1:
        timer_min = st.number_input("Minutes", min_value=0, max_value=180, value=5, step=1)

    with col2:
        timer_sec = st.number_input("Seconds", min_value=0, max_value=59, value=0, step=5)

    with col3:
        st.write("")
        st.write("")
        st.info(f"Set time: {timer_min:02d}:{timer_sec:02d}")

    total_seconds = timer_min * 60 + timer_sec

    timer_html = f"""
    <div style="
        width: 100%;
        max-width: 700px;
        margin: 20px auto;
        padding: 30px;
        border-radius: 20px;
        background: linear-gradient(135deg, #f8fbff, #eef5ff);
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        text-align: center;
        font-family: Arial, sans-serif;
    ">
        <div id="timerDisplay" style="
            font-size: 90px;
            font-weight: 800;
            color: #1f4e79;
            margin-bottom: 25px;
        ">
            {timer_min:02d}:{timer_sec:02d}
        </div>

        <button onclick="startTimer()" style="
            font-size: 24px;
            padding: 12px 28px;
            margin: 8px;
            border: none;
            border-radius: 12px;
            background-color: #2e86de;
            color: white;
            cursor: pointer;
        ">Start</button>

        <button onclick="pauseTimer()" style="
            font-size: 24px;
            padding: 12px 28px;
            margin: 8px;
            border: none;
            border-radius: 12px;
            background-color: #f39c12;
            color: white;
            cursor: pointer;
        ">Pause</button>

        <button onclick="resetTimer()" style="
            font-size: 24px;
            padding: 12px 28px;
            margin: 8px;
            border: none;
            border-radius: 12px;
            background-color: #e74c3c;
            color: white;
            cursor: pointer;
        ">Reset</button>

        <p id="message" style="
            margin-top: 25px;
            font-size: 28px;
            font-weight: bold;
            color: #d63031;
        "></p>
    </div>

    <script>
        let initialTime = {total_seconds};
        let remainingTime = initialTime;
        let timerInterval = null;

        function updateDisplay() {{
            let minutes = Math.floor(remainingTime / 60);
            let seconds = remainingTime % 60;

            document.getElementById("timerDisplay").innerHTML =
                String(minutes).padStart(2, '0') + ":" + String(seconds).padStart(2, '0');
        }}

        function startTimer() {{
            if (timerInterval !== null) {{
                return;
            }}

            document.getElementById("message").innerHTML = "";

            timerInterval = setInterval(function() {{
                if (remainingTime > 0) {{
                    remainingTime--;
                    updateDisplay();
                }} else {{
                    clearInterval(timerInterval);
                    timerInterval = null;
                    document.getElementById("message").innerHTML = "Time's up!";
                    
                    let audio = new Audio("https://actions.google.com/sounds/v1/alarms/beep_short.ogg");
                    audio.play();
                }}
            }}, 1000);
        }}

        function pauseTimer() {{
            clearInterval(timerInterval);
            timerInterval = null;
        }}

        function resetTimer() {{
            clearInterval(timerInterval);
            timerInterval = null;
            remainingTime = initialTime;
            document.getElementById("message").innerHTML = "";
            updateDisplay();
        }}

        updateDisplay();
    </script>
    """

    components.html(timer_html, height=450)

# --- Tab 3: ✅ NEW WordCloud ---
with tabs[4]:
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

# --- Tab 4: (was tabs[4]) TTS ---
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

# --- Tab 6: (was tabs[5]) Drawing ---


# --- Tab 7: (was tabs[6]) Grouping ---
# --- Tab 7: Grouping ---
with tabs[6]:

    st.subheader("👥 Grouping Tool")
    st.caption("CSV를 올리지 않아도 기본 명단으로 조 편성을 할 수 있습니다.")
    st.caption("CSV를 올릴 경우, 반드시 `Course`, `Names` 열이 있어야 합니다.")

    # ---------------------------
    # 기본 명단 데이터
    # CSV를 아직 안 올렸을 때 사용됨
    # ---------------------------
    default_data = pd.DataFrame({
        "Course": [
            "Class 1", "Class 1", "Class 1", "Class 1", "Class 1",
            "Class 1", "Class 1", "Class 1", "Class 1", "Class 1",
            "Class 2", "Class 2", "Class 2", "Class 2", "Class 2",
            "Class 2", "Class 2", "Class 2", "Class 2", "Class 2"
        ],
        "Names": [
            "Student 1", "Student 2", "Student 3", "Student 4", "Student 5",
            "Student 6", "Student 7", "Student 8", "Student 9", "Student 10",
            "Student 11", "Student 12", "Student 13", "Student 14", "Student 15",
            "Student 16", "Student 17", "Student 18", "Student 19", "Student 20"
        ]
    })

    uploaded_file = st.file_uploader("🌱 Step 1: Upload your CSV file (optional)", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        source_label = "✅ Uploaded CSV data"
    else:
        df = default_data
        source_label = "📂 Using default sample data"

    # ---------------------------
    # 데이터 확인
    # ---------------------------
    if all(col in df.columns for col in ["Course", "Names"]):

        st.markdown("### 📋 Current Student List")
        st.dataframe(df, use_container_width=True)

        # Step 2: Select Course
        course_list = df["Course"].dropna().unique().tolist()
        selected_course = st.selectbox("🌱 Step 2: Select Course for Grouping", course_list)

        # 코스별 데이터 필터링 및 인원수 계산
        course_df = df[df["Course"] == selected_course]
        names = course_df["Names"].dropna().tolist()
        total_students = len(names)

        st.info(
            f"{source_label} | 🎓 **{selected_course}**: "
            f"Total **{total_students}** students available for grouping."
        )

        # Step 3: Group size input
        st.markdown("##### 🌱 Step 3: Group Settings")

        col_in1, col_in2 = st.columns(2)

        with col_in1:
            num_group3 = st.number_input(
                "Number of 3-member groups",
                min_value=0,
                value=0,
                step=1
            )

        with col_in2:
            num_group4 = st.number_input(
                "Number of 4-member groups",
                min_value=0,
                value=0,
                step=1
            )

        needed_students = num_group3 * 3 + num_group4 * 4

        st.write(f"Selected students needed: **{needed_students}**")
        st.write(f"Available students: **{total_students}**")

        if needed_students > total_students:
            st.warning("설정한 조 인원 수가 현재 학생 수보다 많습니다. 조 개수를 줄여 주세요.")

        # Step 4: Generate Groups
        if st.button("🌱 Step 4: Generate Groups"):

            if total_students == 0:
                st.warning("No students available for grouping.")

            elif num_group3 == 0 and num_group4 == 0:
                st.warning("Please enter at least one group.")

            else:
                names_for_grouping = names.copy()
                random.shuffle(names_for_grouping)

                grouped_data = []
                group_num = 1
                assigned_count = 0

                # 1. 3인 그룹 생성
                for _ in range(num_group3):
                    if len(names_for_grouping) >= 3:
                        members = names_for_grouping[:3]
                        names_for_grouping = names_for_grouping[3:]

                        group_row = {"Group": f"Group {group_num}"}
                        for i, member in enumerate(members):
                            group_row[f"Member{i+1}"] = member

                        grouped_data.append(group_row)
                        group_num += 1
                        assigned_count += 3

                # 2. 4인 그룹 생성
                for _ in range(num_group4):
                    if len(names_for_grouping) >= 4:
                        members = names_for_grouping[:4]
                        names_for_grouping = names_for_grouping[4:]

                        group_row = {"Group": f"Group {group_num}"}
                        for i, member in enumerate(members):
                            group_row[f"Member{i+1}"] = member

                        grouped_data.append(group_row)
                        group_num += 1
                        assigned_count += 4

                # 3. 남은 인원 처리
                remaining_count = len(names_for_grouping)

                if remaining_count > 0:
                    group_row = {"Group": f"Group {group_num} (Remainder)"}
                    for i, member in enumerate(names_for_grouping):
                        group_row[f"Member{i+1}"] = member

                    grouped_data.append(group_row)
                    assigned_count += remaining_count

                if not grouped_data:
                    st.warning("No groups were created. Please check your settings.")

                else:
                    grouped_df = pd.DataFrame(grouped_data)

                    cols = ["Group"] + [
                        c for c in grouped_df.columns if c.startswith("Member")
                    ]

                    grouped_df = grouped_df[cols].fillna("")

                    st.success(
                        f"✅ Grouping Complete! "
                        f"Total {assigned_count} students assigned to {len(grouped_data)} groups."
                    )

                    st.dataframe(grouped_df, use_container_width=True)

                    # 다운로드 버튼
                    csv_text = grouped_df.to_csv(index=False)
                    csv_bytes = csv_text.encode("utf-8-sig")

                    st.download_button(
                        label="📥 Download Grouped CSV",
                        data=csv_bytes,
                        file_name=f"grouped_{selected_course.replace(' ', '_')}.csv",
                        mime="text/csv"
                    )

    else:
        st.error("The file must contain both `Course` and `Names` columns.")
