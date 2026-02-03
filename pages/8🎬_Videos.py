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

def render_video_player(video_dict: dict, sidebar_key: str, sidebar_title: str):
    """
    video_dict: {label: url}
    sidebar_key: unique key per tab (prevents widget collision)
    sidebar_title: title shown in sidebar
    """
    st.sidebar.header(sidebar_title)

    labels = list(video_dict.keys())
    if not labels:
        st.warning("No videos available.")
        return

    # ✅ unique selectbox key per tab
    selected = st.sidebar.selectbox(
        "Select",
        labels,
        index=0,
        label_visibility="collapsed",
        key=sidebar_key,
    )

    st.sidebar.caption("Link")
    st.sidebar.code(video_dict[selected], language="text")

    st.sidebar.markdown(
        f"""
        <a href="{video_dict[selected]}" target="_blank" rel="noopener noreferrer"
           style="text-decoration:none;">
           ▶️ Open on YouTube
        </a>
        """,
        unsafe_allow_html=True,
    )

    st.subheader(f"Now Playing: {selected}")

    embed = youtube_embed_url(video_dict[selected])
    if not embed:
        st.error("Invalid YouTube link format. Please check the URL in the sidebar.")
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


# ---------- Tab 1 videos (your original list) ----------
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

# ---------- Tab 2 videos (Class videos) ----------
CLASS_VIDEOS = {
    "Week 01 · Orientation": "https://www.youtube.com/watch?v=VIDEO_ID_A",
    "Week 02 · Digital tools overview": "https://www.youtube.com/watch?v=VIDEO_ID_B",
    # 필요하면 계속 추가
}

# ---------- Tabs ----------
tab1, tab2 = st.tabs(["Video Library", "Class videos"])

# ✅ 핵심: sidebar는 페이지 전체에서 공유되므로
#    '현재 활성 탭'에 맞는 sidebar UI만 출력해야 충돌이 없습니다.
#    -> 탭별로 렌더링 함수를 호출하되, selectbox key를 다르게.

with tab1:
    st.caption("🎬 Select a video from the left menu to play it here.")
    render_video_player(
        video_dict=VIDEOS,
        sidebar_key="sidebar_select_video_library",  # ✅ unique key
        sidebar_title="Choose a video",
    )

with tab2:
    st.caption("🎓 Class videos (select from the left menu).")
    render_video_player(
        video_dict=CLASS_VIDEOS,
        sidebar_key="sidebar_select_class_videos",   # ✅ unique key
        sidebar_title="Choose a class video",
    )
