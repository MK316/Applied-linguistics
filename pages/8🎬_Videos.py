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

# ---------- Video lists ----------
VIDEOS = {
    "SW교육과 AI교육, 왜 배워야 할까요?": "https://youtu.be/lQ2kAukmWQE?si=-m1vxlwy46tQGrTp",
    "2015-1": "https://www.youtube.com/watch?v=VIDEO_ID_2",
    "2005-2": "https://www.youtube.com/watch?v=VIDEO_ID_3",
}

CLASS_VIDEOS = {
    "Week 01 · Orientation": "https://www.youtube.com/watch?v=VIDEO_ID_A",
    "Week 02 · Digital tools overview": "https://www.youtube.com/watch?v=VIDEO_ID_B",
}

# ---------- "Tabs" selector (acts like tabs, but controllable) ----------
# Streamlit 버전에 따라 segmented_control이 없을 수 있어 fallback 포함
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

# ---------- Sidebar: show ONLY ONE menu depending on view ----------
if view == "Video Library":
    st.sidebar.header("Choose a video")
    labels = list(VIDEOS.keys())
    selected = st.sidebar.selectbox(
        "Select",
        labels,
        index=0,
        key="sidebar_video_library_select",
        label_visibility="collapsed",
    )
    st.sidebar.caption("Link")
    st.sidebar.code(VIDEOS[selected], language="text")
    st.sidebar.markdown(
        f"""<a href="{VIDEOS[selected]}" target="_blank" rel="noopener noreferrer"
            style="text-decoration:none;">▶️ Open on YouTube</a>""",
        unsafe_allow_html=True,
    )

    render_player(selected, VIDEOS[selected])

else:  # Class videos
    st.sidebar.header("Choose a class video")
    labels = list(CLASS_VIDEOS.keys())
    selected = st.sidebar.selectbox(
        "Select",
        labels,
        index=0,
        key="sidebar_class_videos_select",
        label_visibility="collapsed",
    )
    st.sidebar.caption("Link")
    st.sidebar.code(CLASS_VIDEOS[selected], language="text")
    st.sidebar.markdown(
        f"""<a href="{CLASS_VIDEOS[selected]}" target="_blank" rel="noopener noreferrer"
            style="text-decoration:none;">▶️ Open on YouTube</a>""",
        unsafe_allow_html=True,
    )

    render_player(selected, CLASS_VIDEOS[selected])
