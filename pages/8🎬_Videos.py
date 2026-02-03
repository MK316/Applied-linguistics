import streamlit as st
import re

st.set_page_config(page_title="Video Library", layout="wide")

# ---------- Helpers ----------
def extract_youtube_id(url: str) -> str | None:
    patterns = [
        r"(?:v=)([A-Za-z0-9_-]{11})",
        r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:embed/)([A-Za-z0-9_-]{11})",
        r"(?:shorts/)([A-Za-z0-9_-]{11})",
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None

def youtube_embed_url(url: str) -> str:
    vid = extract_youtube_id(url)
    return f"https://www.youtube.com/embed/{vid}?rel=0&modestbranding=1" if vid else ""

def render_player(selected_label: str, selected_url: str):
    st.subheader(f"Now Playing: {selected_label}")

    embed = youtube_embed_url(selected_url)
    if not embed:
        st.error("Invalid YouTube link format. Please check the URL.")
        return

    st.markdown(
        """
        <style>
        .video-wrap {
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            aspect-ratio: 16 / 9;
            border-radius: 14px;
            overflow: hidden;
            box-shadow: 0 6px 20px rgba(0,0,0,0.12);
            background: #000;
        }
        .video-wrap iframe {
            width: 100%;
            height: 100%;
            border: 0;
        }
        .meta-box {
            width: 100%;
            max-width: 1200px;
            margin: 0.75rem auto 0;
            padding: 0.75rem 1rem;
            border-radius: 12px;
            background: rgba(0,0,0,0.03);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="video-wrap">
          <iframe src="{embed}"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                  allowfullscreen>
          </iframe>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------- Video lists (label -> {url, caption}) ----------
VIDEOS = {
    "SW교육과 AI교육, 왜 배워야 할까요?": {
        "url": "https://youtu.be/lQ2kAukmWQE?si=-m1vxlwy46tQGrTp",
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
    "Week 01 · Orientation": {
        "url": "https://www.youtube.com/watch?v=VIDEO_ID_A",
        "caption": "수업 목표, 평가 방식, 프로젝트 개요 안내",
    },
    "Week 02 · Digital tools overview": {
        "url": "https://www.youtube.com/watch?v=VIDEO_ID_B",
        "caption": "수업에서 사용할 디지털 도구와 활동 흐름 소개",
    },
}

# ---------- "Tabs" selector (segmented if available; fallback to radio) ----------
try:
    view = st.segmented_control(
        "View",
        options=["Video Library", "Class videos"],
        default="Video Library",
        label_visibility="collapsed",
    )
except Exception:
    view = st.radio(
        "View",
        options=["Video Library", "Class videos"],
        horizontal=True,
        label_visibility="collapsed",
    )

st.caption("🎬 Select a video from the left menu to play it here.")

# ---------- Sidebar + Main (show ONLY one menu depending on view) ----------
if view == "Video Library":
    st.sidebar.header("Choose a video")

    labels = list(VIDEOS.keys())
    if not labels:
        st.warning("No videos available in Video Library.")
    else:
        selected = st.sidebar.selectbox(
            "Select",
            labels,
            index=0,
            key="sidebar_video_library_select",
            label_visibility="collapsed",
        )

        selected_url = VIDEOS[selected]["url"]
        selected_caption = VIDEOS[selected].get("caption", "")

        st.sidebar.caption("Link")
        st.sidebar.code(selected_url, language="text")

        st.sidebar.markdown(
            f"""<a href="{selected_url}" target="_blank" rel="noopener noreferrer"
                style="text-decoration:none;">▶️ Open on YouTube</a>""",
            unsafe_allow_html=True,
        )

        st.subheader(f"Now Playing: {selected}")
        if selected_caption:
            st.caption(selected_caption)

        render_player(selected, selected_url)

else:  # Class videos
    st.sidebar.header("Choose a class video")

    labels = list(CLASS_VIDEOS.keys())
    if not labels:
        st.warning("No videos available in Class videos.")
    else:
        selected = st.sidebar.selectbox(
            "Select",
            labels,
            index=0,
            key="sidebar_class_videos_select",
            label_visibility="collapsed",
        )

        selected_url = CLASS_VIDEOS[selected]["url"]
        selected_caption = CLASS_VIDEOS[selected].get("caption", "")

        st.sidebar.caption("Link")
        st.sidebar.code(selected_url, language="text")

        st.sidebar.markdown(
            f"""<a href="{selected_url}" target="_blank" rel="noopener noreferrer"
                style="text-decoration:none;">▶️ Open on YouTube</a>""",
            unsafe_allow_html=True,
        )

        st.subheader(f"Now Playing: {selected}")
        if selected_caption:
            st.caption(selected_caption)

        render_player(selected, selected_url)
