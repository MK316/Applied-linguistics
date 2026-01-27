import re
import requests
import streamlit as st

st.set_page_config(layout="wide")

# =========================
# Repo config
# =========================
OWNER = "MK316"
REPO = "Applied-linguistics"
BRANCH = "main"

RAW_BASE = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}"
API_BASE = f"https://api.github.com/repos/{OWNER}/{REPO}/contents"

# Each tab points to a folder. (No n / prefix needed.)
SLIDE_SETS = {
    "Ch 1": {"folder": "lectureslides/test"},
    "Ch 2": {"folder": "lectureslides/intro"},
    "Ch 3": {"folder": "lectureslides/ch03"},
}

# =========================
# Helpers
# =========================
def extract_numbers(s: str):
    """Return a tuple of ints found in filename for robust sorting."""
    nums = re.findall(r"\d+", s)
    return tuple(int(x) for x in nums) if nums else (10**9,)

@st.cache_data(show_spinner=False)
def list_png_files_in_folder(folder: str):
    """
    Lists .png files in a GitHub folder using GitHub Contents API.
    Returns a list of filenames sorted by numbers in the name.
    """
    url = f"{API_BASE}/{folder}?ref={BRANCH}"
    r = requests.get(url, timeout=15)
    if r.status_code != 200:
        return [], f"GitHub API error {r.status_code}: {r.text[:200]}"
    data = r.json()
    if not isinstance(data, list):
        return [], "Unexpected API response (not a folder listing)."

    pngs = [item["name"] for item in data
            if item.get("type") == "file"
            and item.get("name", "").lower().endswith(".png")]

    # Sort: primarily by numbers in filename, secondarily by name
    pngs.sort(key=lambda name: (extract_numbers(name), name.lower()))
    return pngs, None

def init_state(key: str, default):
    if key not in st.session_state:
        st.session_state[key] = default

def clamp(x: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, x))

def go_prev(idx_key: str, sel_key: str, n: int):
    st.session_state[idx_key] = clamp(st.session_state[idx_key] - 1, 1, n)
    st.session_state[sel_key] = st.session_state[idx_key]

def go_next(idx_key: str, sel_key: str, n: int):
    st.session_state[idx_key] = clamp(st.session_state[idx_key] + 1, 1, n)
    st.session_state[sel_key] = st.session_state[idx_key]

def sync_from_select(idx_key: str, sel_key: str):
    st.session_state[idx_key] = int(st.session_state[sel_key])

# =========================
# UI
# =========================
st.markdown("#### Applied Linguistics (Spring 2026)")
st.caption("Lecture slide viewer")

tab_labels = list(SLIDE_SETS.keys())
tabs = st.tabs(tab_labels)

for tab, label in zip(tabs, tab_labels):
    folder = SLIDE_SETS[label]["folder"]

    # Load files for this folder
    files, err = list_png_files_in_folder(folder)

    idx_key = f"idx__{label}"
    sel_key = f"sel__{label}"
    init_state(idx_key, 1)
    init_state(sel_key, st.session_state[idx_key])

    with tab:
        if err:
            st.error(f"Could not load slides from `{folder}`.\n\n{err}")
            continue

        if not files:
            st.warning(f"No PNG files found in `{folder}`.")
            continue

        n = len(files)

        # Keep index safe if files count changed
        st.session_state[idx_key] = clamp(int(st.session_state[idx_key]), 1, n)
        st.session_state[sel_key] = st.session_state[idx_key]

        # Controls
        c1, c2, c3 = st.columns([1.2, 1.2, 3.0], vertical_alignment="bottom")

        with c1:
            st.button(
                "◀ Previous",
                use_container_width=True,
                key=f"btn_prev__{label}",
                on_click=go_prev,
                args=(idx_key, sel_key, n),
            )

        with c2:
            st.button(
                "Next ▶",
                use_container_width=True,
                key=f"btn_next__{label}",
                on_click=go_next,
                args=(idx_key, sel_key, n),
            )

        with c3:
            st.markdown("<div style='height: 2px;'></div>", unsafe_allow_html=True)
            st.selectbox(
                "Select slide",
                options=list(range(1, n + 1)),
                key=sel_key,
                index=st.session_state[idx_key] - 1,
                on_change=sync_from_select,
                args=(idx_key, sel_key),
                label_visibility="collapsed",
            )

        # Display
        idx = int(st.session_state[idx_key])
        filename = files[idx - 1]
        url = f"{RAW_BASE}/{folder}/{filename}"

        st.markdown(f"**{label}** · Slide **{idx} / {n}**")

        # Fit by viewport height (no vertical cutoff)
        st.markdown(
            f"""
            <div style="display:flex; justify-content:center;">
              <img src="{url}"
                   style="max-height: 80vh; width:auto; max-width:100%; object-fit:contain;">
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Optional: show filename quietly (remove if you prefer)
        st.caption(filename)
