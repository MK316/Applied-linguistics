import streamlit as st
import re

# ---------- Page setup ----------
st.set_page_config(page_title="Video Library", layout="wide")

st.title("🎬 Video Library")
st.caption("Select a video from the dropdown to play it on this page.")

# ---------- Video list (label -> YouTube URL) ----------
VIDEOS = {
    "2016-3": "https://www.youtube.com/watch?v=VIDEO_ID_1",
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
    """Extract YouTube video ID from common URL patterns."""
    patterns = [
        r"(?:v=)([A-Za-z0-9_-]{11})",          # watch?v=xxxxxxxxxxx
        r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",  # youtu.be/xxxxxxxxxxx
        r"(?:embed/)([A-Za-z0-9_-]{11})",      # /embed/xxxxxxxxxxx
        r"(?:shorts/)([A-Za-z0-9_-]{11})",     # /shorts/xxxxxxxxxxx
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None

def youtube_embed_url(url: str) -> str:
    vid = extract_youtube_id(url)
    if not vid:
        return ""
    # modestbranding + rel=0 for cleaner player
    return f"https://www.youtube.com/embed/{vid}?rel=0&modestbranding=1"

# ---------- UI: controls ----------
left, right = st.columns([1.2, 3.8], vertical_alignment="top")

with left:
    st.subheader("Choose")
    options = list(VIDEOS.keys())
    selected = st.selectbox("Select a video", options, index=0, label_visibility="collapsed")

    # Optional: show the raw link for copying
    st.caption("Link")
    st.code(VIDEOS[selected], language="text")

with right:
    st.subheader(f"Now Playing: {selected}")

    embed = youtube_embed_url(VIDEOS[selected])
    if not embed:
        st.error("Invalid YouTube link format. Please check the URL.")
    else:
        # Clean, responsive container
        st.markdown(
            """
            <style>
            .video-wrap {
                width: 100%;
                max-width: 1100px;
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
