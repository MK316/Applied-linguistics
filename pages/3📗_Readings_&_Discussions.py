import streamlit as st
import requests
import re

# --- 1. 페이지 설정 (레이아웃을 넓게 설정) ---
st.set_page_config(page_title="Readings and in-class discussion", layout="wide")

# ---------- [헬퍼 함수: 유튜브 및 마크다운 처리] ----------
def extract_youtube_id(url: str) -> str | None:
    patterns = [
        r"(?:v=)([A-Za-z0-9_-]{11})",
        r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:embed/)([A-Za-z0-9_-]{11})",
        r"(?:shorts/)([A-Za-z0-9_-]{11})",
    ]
    for p in patterns:
        m = re.search(p, url)
        if m: return m.group(1)
    return None

def youtube_embed_url(url: str) -> str:
    vid = extract_youtube_id(url)
    return f"https://www.youtube.com/embed/{vid}?rel=0&modestbranding=1" if vid else ""

def render_player(selected_url: str):
    embed = youtube_embed_url(selected_url)
    if not embed:
        st.error("Invalid YouTube link format. Please check the URL.")
        return
    st.markdown(
        f"""
        <style>
        .video-wrap {{
            width: 100%;
            max-width: 1000px;
            margin: 0 auto;
            aspect-ratio: 16 / 9;
            border-radius: 14px;
            overflow: hidden;
            box-shadow: 0 6px 20px rgba(0,0,0,0.12);
            background: #000;
        }}
        .video-wrap iframe {{
            width: 100%;
            height: 100%;
            border: 0;
        }}
        </style>
        <div class="video-wrap">
          <iframe src="{embed}" 
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                  allowfullscreen>
          </iframe>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------- [데이터베이스: 비디오 및 요약본 리스트] ----------
VIDEOS = {
    "SW교육과 AI교육, 왜 배워야 할까요?": {
        "url": "https://youtu.be/lQ2kAukmWQE",
        "caption": "AI 시대에 왜 SW·AI 교육이 중요한지 개관하는 입문 영상",
    },
    "2015-1": {
        "url": "https://www.youtube.com/watch?v=VIDEO_ID_2",
        "caption": "임용 대비 핵심 개념 정리(예시 캡션).",
    },
    "2005-2": {
        "url": "https://www.youtube.com/watch?v=VIDEO_ID_3",
        "caption": "기출 유형 분석(예시 캡션).",
    },
}

CLASS_VIDEOS = {
    "Week 01a · From Teacher to Creator": {
        "url": "https://youtu.be/ya0trJ6qtOw",
        "caption": "Becoming a teacher-designer who shapes the learning environment through AI collaboration",
    },
    "Week 01b · Humanistic Horizon: for English educator": {
        "url": "https://youtu.be/pKKR7RVBlc0",
        "caption": "수업에서 사용할 디지털 도구와 활동 흐름 소개",
    },
    "Week 02a · Digital Mind: Alignment problem (easier version)": {
        "url": "https://youtu.be/U8CwEvGeU_A",
        "caption": "디지털 사고에 대한 이해 및 인간의 가치 문제",
    },
    "Week 02b · Alignment Problem: Curry et al. (2025)": {
        "url": "https://youtu.be/JqBV-wug-WQ",
        "caption": "인간의 지식처리와 인공지능의 데이터처리 방식",
    },    
     "Week 03 · CT and Literacy: Jacob & Warschauer (2018)": {
        "url": "https://youtu.be/bRVTDYAfj3M",
        "caption": "인공지능 시대의 새로운 문해력 정의 및 접근방식",
    },  
}

# Reading Summary 파일 목록 (파일명이 정확해야 함)
SUMMARY_FILES = {
    "Select a summary...": None,
    "Reading #1: Translanguaging (Li, 2018)": "Reading01_summary.md",
    "Reading #2: Alignment Issues (Curry, 2025)": "Reading02_summary.md",
    "Reading #3: Computational Thinking (Jacob, 2018)": "Reading03_summary.md",
    "Reading #5: AI in Higher Education (Zawacki, 2019)": "Reading05_summary.md",
}

# --- 2. 탭 생성 ---
tab_labels = ["🏠 Reading list", "🌱 Core idea", "💦 In-class presentation", "🖼️ Infographics", "📝 Reading Summary", "🎬 Video"]
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(tab_labels)

# --- 3. 탭별 콘텐츠 구성 ---

with tab1:
    st.markdown("### 🔖 Reading list")
    st.caption("To be updated continuously")
    st.markdown("""
      + Reading #1: Translanguaging [Li, Wei (2018)](https://www.researchgate.net/publication/323720294_Translanguaging_as_a_Practical_Theory_of_Language) 📓 [Handout](https://github.com/MK316/Collaboration26/raw/main/Hanouts/CH01_handout.pdf)
      + Reading #2: Alignment issues [Curry et al. (2025)](https://github.com/MK316/Applied-linguistics/raw/main/readings/02_Curry_etal_2025.pdf) 📓 [Handout](https://github.com/MK316/Collaboration26/raw/main/Hanouts/Reading01_Summary_handout.pdf)
      + Reading #3: [Jacob, S. R. & M. Warschauer](https://www.researchgate.net/publication/327217492_Computational_Thinking_and_Literacy) (2018). Computational Thinking and Literacy. _Journal of Computer Science Integration_, 1(1).
      + Reading #4: [UNESCO](https://www.unesco.org/en/digital-education/artificial-intelligence) (2025) _AI in education_.
      + Reading #5: [Zawacki-Richter et al. (2019)](https://www.researchgate.net/publication/336846972_Systematic_review_of_research_on_artificial_intelligence_applications_in_higher_education_-where_are_the_educators) Zawacki-Richter, O., Marín, V. I., Bond, M., & Gouverneur, F. (2019). Systematic review of research on artificial intelligence applications in higher education. _International Journal of Educational Technology in Higher Education_, 16(1), 1–27.
      + Reading #6: [Jeon et al.](https://www.researchgate.net/publication/394128596_Generative_AI_and_its_dilemmas_Exploring_AI_from_a_translanguaging_perspective) (2025). Generative AI and its dilemmas: exploring AI from a translanguaging perspective. _Applied Linguistics_, 46, 709-717.
      + Reading #7: [Lai et al. (2025)](https://academic.oup.com/applij/article/46/1/128/7420497) Purpose and strategic engagement in informal English digital activities and aspects of vocabulary knowledge. _Applied Linguistics_ 46, 128-145.
      + Reading #8: [Mishra & Koehler (2006)](https://rediie.cl/wp-content/uploads/Mishra-Koehler.pdf) Mishra, P., & Koehler, M. J. (2006). Technological pedagogical content knowledge: A framework for teacher knowledge. _Teachers College Record_, 108(6), 1017–1054.
    
      📗 Supplementary book: _An Introduction to Applied Linguistics_ (2007; 2nd ed.) by A. Davies, Edinburgh University Press.
      [Book cover](https://pasca.uns.ac.id/s3linguistik/wp-content/uploads/sites/44/2016/10/an-introduction-to-applied-linguistics.pdf)

      + [Chapter 1 slides](https://github.com/MK316/Applied-linguistics/raw/main/lectureslides/chapter1/CH01_Slides.pdf): History and 'definitions'
      """)

with tab2:
    url = "https://raw.githubusercontent.com/MK316/Applied-linguistics/main/mdfiles/Core-idea.md"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            st.markdown(response.text)
        else:
            st.error(f"파일을 불러오지 못했습니다. (HTTP {response.status_code})")
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")

with tab3:
    st.caption("Fetching the latest documentation from Github [Collaboration26](https://github.com/MK316/Collaboration26).")
    readme_url = "https://raw.githubusercontent.com/MK316/Collaboration26/main/README.md"
    try:
        response = requests.get(readme_url)
        if response.status_code == 200:
            st.markdown(response.text)
        else:
            st.error(f"Failed to load the README file. (HTTP {response.status_code})")
    except Exception as e:
        st.error(f"An error occurred while fetching the file: {e}")

with tab4:
    image_options = {
        "Select an image...": None,
        "Supplementary book Chapter 1": "https://raw.githubusercontent.com/MK316/Collaboration26/main/infographic/CH01_infographic.png",
        "Reading #1": "https://raw.githubusercontent.com/MK316/Collaboration26/main/infographic/Reading01_infographic.png",
        "Reading #2": "https://raw.githubusercontent.com/MK316/Collaboration26/main/infographic/Reading02_infographic.png",
        "Reading #3": "https://raw.githubusercontent.com/MK316/Collaboration26/main/infographic/Reading03_infographic.png",
        "Reading #4": "https://raw.githubusercontent.com/MK316/Collaboration26/main/infographic/Reading04_infographic.png",
        "Reading #5": "https://raw.githubusercontent.com/MK316/Collaboration26/main/infographic/Reading05_infographic.png",
        "Reading #6": "https://raw.githubusercontent.com/MK316/Collaboration26/main/infographic/Reading06_infographic.png",
    }
    selected_image_name = st.selectbox("Choose an image to display:", options=list(image_options.keys()), key="img_select")
    if selected_image_name and image_options[selected_image_name]:
        image_url = image_options[selected_image_name]
        st.divider()
        st.subheader(f"Viewing: {selected_image_name}")
        st.image(image_url, caption=f"Source: {selected_image_name}", use_container_width=True)
        st.caption(f"[Open original image in new tab]({image_url})")
    else:
        st.info("Please select an image from the dropdown menu above.")

# 📝 4. Reading Summary 탭 (Infographics와 Video 사이에 위치)
with tab5:
    st.markdown("### 📝 Reading Summary")
    st.caption("Github [Collaboration26/Reading_summary](https://github.com/MK316/Collaboration26/tree/main/Reading_summary)")
    
    selected_summary = st.selectbox("Choose a Reading Summary to display:", options=list(SUMMARY_FILES.keys()), key="summary_select")
    
    if selected_summary and SUMMARY_FILES[selected_summary]:
        file_name = SUMMARY_FILES[selected_summary]
        raw_summary_url = f"https://raw.githubusercontent.com/MK316/Collaboration26/main/Reading_summary/{file_name}"
        
        try:
            with st.spinner('Loading summary content...'):
                response = requests.get(raw_summary_url)
                if response.status_code == 200:
                    st.divider()
                    st.markdown(response.text)
                else:
                    st.error(f"파일을 가져오지 못했습니다. (HTTP {response.status_code})")
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
    else:
        st.info("드롭다운 메뉴에서 읽고 싶은 요약본을 선택하세요.")

# 🎬 5. Video 탭
with tab6:
    st.markdown("### 🎬 Class Video Library")
    
    try:
        view = st.segmented_control(
            "Video Category",
            options=["Video Library", "Class videos"],
            default="Video Library",
            label_visibility="collapsed"
        )
    except:
        view = st.radio("Category:", options=["Video Library", "Class videos"], horizontal=True, label_visibility="collapsed")

    dataset = VIDEOS if view == "Video Library" else CLASS_VIDEOS
    
    v_col1, v_col2 = st.columns([1, 2.5])
    
    with v_col1:
        st.subheader("📋 Playlist")
        selected_label = st.selectbox("Select a video:", options=list(dataset.keys()), key="video_final_selector")
        target = dataset[selected_label]
        st.info(f"**Caption:** {target.get('caption', '')}")
        st.markdown(f"[Watch on YouTube ▶️]({target['url']})")

    with v_col2:
        st.subheader(f"📺 Playing: {selected_label}")
        render_player(target['url'])
