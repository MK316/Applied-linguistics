import streamlit as st
import re

st.set_page_config(page_title="Video Library", layout="wide")

st.caption("🎬 Select a video from the left menu to play it here.")

# ---------- Video list (label -> YouTube URL) ----------
VIDEOS = {
    "SW교육과 AI교육, 왜 배워야 할까요?": "https://youtu.be/lQ2kAukmWQE?si=-m1vxlwy46tQGrTp",
    "2015-1": "https://www.youtube.com/watch?v=VIDEO_ID_2",
    "2005-2": "https://www.youtube.com/watch?v=VIDEO_ID_3",
    "2013-2": "https://www.youtube.com/watch?v=VIDEO_ID_4",
    "2015-2": "https://www.youtube.com/watch?v=VIDEO_ID_5",
    "2005-1": "https://www.youtube.com/watch?v=VIDEO_ID_6",
    "2008-2": "https://www.youtube.com/watch?v=VIDEO_ID_7",
    "2007-1": "https://www.youtube.com/watch?v=VIDEO_ID_8",
    "2012-2": "https://www.youtube.com/watch?v=VIDEO_ID_9",
    "2011-1": "https://www.youtube.com/watch?v=VIDEO_ID_10",
    "2020-2": "https://www.youtube.com/watch?v=VIDEO_ID_11",
    "2018-3": "https://www.youtube.com/watch?v=VIDEO_ID_12",
}

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

# ---------- Sidebar (Left Menu) ----------
st.sidebar.header("Choose a video")

labels = list(VIDEOS.keys())
selected = st.sidebar.selectbox("Select", labels, index=0, label_visibility="collapsed")

st.sidebar.caption("Link")
st.sidebar.code(VIDEOS[selected], language="text")

# Optional: open in YouTube
st.sidebar.markdown(
    f"""
    <a href="{VIDEOS[selected]}" target="_blank" rel="noopener noreferrer"
       style="text-decoration:none;">
       ▶️ Open on YouTube
    </a>
    """,
    unsafe_allow_html=True,
)

# ---------- Main display ----------
st.subheader(f"Now Playing: {selected}")

embed = youtube_embed_url(VIDEOS[selected])
if not embed:
    st.error("Invalid YouTube link format. Please check the URL in the sidebar.")
else:
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
