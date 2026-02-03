import re
import requests
import streamlit as st

st.set_page_config(layout="wide")

OWNER = "MK316"
REPO = "Applied-linguistics"
BRANCH = "main"

RAW_BASE = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}"
API_BASE = f"https://api.github.com/repos/{OWNER}/{REPO}/contents"

SLIDE_SETS = {
    "Intro": {"folder": "lectureslides/intro"},
    "Ch 2": {"folder": "lectureslides/test"},
    "Ch 3": {"folder": "lectureslides/ch03"},
}

# ---------- Helpers ----------
def extract_numbers(s: str):
    nums = re.findall(r"\d+", s)
    return tuple(int(x) for x in nums) if nums else (10**9,)

@st.cache_data(ttl=3600, show_spinner=False)
def list_png_files_in_folder(folder: str):
    headers = {}
    token = st.secrets.get("GITHUB_TOKEN", None)
    if token:
        headers["Authorization"] = f"token {token}"

    url = f"{API_BASE}/{folder}?ref={BRANCH}"
    r = requests.get(url, headers=headers, timeout=15)

    if r.status_code != 200:
        return [], f"GitHub API error {r.status_code}: {r.text[:200]}"

    data = r.json()
    if not isinstance(data, list):
        return [], "Unexpected API response (not a folder listing)."

    pngs = [
        item["name"] for item in data
        if item.get("type") == "file"
        and item.get("name", "").lower().endswith(".png")
    ]
    pngs.sort(key=lambda name: (extract_numbers(name), name.lower()))
    return pngs, None

def clamp(x: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, x))

def go_prev(idx_key: str, n: int):
    st.session_state[idx_key] = clamp(int(st.session_state[idx_key]) - 1, 1, n)

def go_next(idx_key: str, n: int):
    st.session_state[idx_key] = clamp(int(st.session_state[idx_key]) + 1, 1, n)

# ---------- UI ----------
st.markdown("#### Applied Linguistics (Spring 2026)")
st.caption("Lecture slide viewer")

tab_labels = list(SLIDE_SETS.keys())
tabs = st.tabs(tab_labels)

for tab, label in zip(tabs, tab_labels):
    folder = SLIDE_SETS[label]["folder"]
    files, err = list_png_files_in_folder(folder)

    idx_key = f"idx__{label}"  # ✅ the ONLY state key per tab

    with tab:
        if err:
            st.error(f"Could not load slides from `{folder}`.\n\n{err}")
            continue
        if not files:
            st.warning(f"No PNG files found in `{folder}`.")
            continue

        n = len(files)

        # initialize once
        if idx_key not in st.session_state:
            st.session_state[idx_key] = 1
        st.session_state[idx_key] = clamp(int(st.session_state[idx_key]), 1, n)

        # Controls (aligned)
        c1, c2, c3 = st.columns([1.2, 1.2, 3.0], vertical_alignment="bottom")

        with c1:
            st.button(
                "◀ Previous",
                use_container_width=True,
                key=f"btn_prev__{label}",
                on_click=go_prev,
                args=(idx_key, n),
            )

        with c2:
            st.button(
                "Next ▶",
                use_container_width=True,
                key=f"btn_next__{label}",
                on_click=go_next,
                args=(idx_key, n),
            )

        with c3:
            st.markdown("<div style='height: 2px;'></div>", unsafe_allow_html=True)
            st.selectbox(
                "Select slide",
                options=list(range(1, n + 1)),
                key=idx_key,                 # ✅ same key as slide index
                label_visibility="collapsed",
            )

        # Display
        idx = int(st.session_state[idx_key])
        filename = files[idx - 1]
        url = f"{RAW_BASE}/{folder}/{filename}"

        st.markdown(f"**{label}** · Slide **{idx} / {n}**")

        st.markdown(
            f"""
            <div style="display:flex; justify-content:center;">
              <img src="{url}"
                   style="max-height: 80vh; width:auto; max-width:100%; object-fit:contain;">
            </div>
            """,
            unsafe_allow_html=True,
        )
