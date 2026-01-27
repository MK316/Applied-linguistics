import streamlit as st

# =========================
# Config
# =========================
RAW_BASE = "https://raw.githubusercontent.com/MK316/Applied-linguistics/main"

SLIDE_SETS = {
    "Ch 1": {"folder": "lectureslides/test", "n": 2, "prefix": "test.", "ext": "png"},
    "Ch 2": {"folder": "lectureslides/ch02", "n": 18, "prefix": "slide_", "ext": "png"},
    "Ch 3": {"folder": "lectureslides/ch03", "n": 30, "prefix": "slide_", "ext": "png"},
}

# =========================
# Helpers
# =========================
def slide_url(folder: str, idx: int, prefix: str, ext: str) -> str:
    return f"{RAW_BASE}/{folder}/{prefix}{idx:03d}.{ext}"

def init_state(key: str, default):
    if key not in st.session_state:
        st.session_state[key] = default

def clamp(x: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, x))

def go_prev():
    chapter = st.session_state["chapter"]
    n = SLIDE_SETS[chapter]["n"]
    idx_key = f"idx__{chapter}"
    st.session_state[idx_key] = clamp(st.session_state[idx_key] - 1, 1, n)
    st.session_state["slide_select"] = st.session_state[idx_key]  # sync dropdown

def go_next():
    chapter = st.session_state["chapter"]
    n = SLIDE_SETS[chapter]["n"]
    idx_key = f"idx__{chapter}"
    st.session_state[idx_key] = clamp(st.session_state[idx_key] + 1, 1, n)
    st.session_state["slide_select"] = st.session_state[idx_key]  # sync dropdown

# =========================
# UI
# =========================
st.markdown("#### Applied Linguistics (Spring 2026)")
st.caption("Lecture slide viewer")

# --- Chapter selector (acts like tabs) ---
init_state("chapter", list(SLIDE_SETS.keys())[0])

chapter = st.radio(
    "Chapter",
    options=list(SLIDE_SETS.keys()),
    horizontal=True,
    key="chapter",
    label_visibility="collapsed",
)

cfg = SLIDE_SETS[chapter]
folder, n, prefix, ext = cfg["folder"], cfg["n"], cfg["prefix"], cfg["ext"]

# per-chapter slide index state
idx_key = f"idx__{chapter}"
init_state(idx_key, 1)

# --- Sidebar: ONE selectbox only (for active chapter) ---
with st.sidebar:
    st.markdown(f"### {chapter}")
    # keep sidebar selectbox synced to current idx on each rerun
    init_state("slide_select", st.session_state[idx_key])
    st.session_state["slide_select"] = st.session_state[idx_key]

    selected = st.selectbox(
        "Select slide",
        options=list(range(1, n + 1)),
        index=st.session_state[idx_key] - 1,
        key="slide_select",
    )

    # if user changed dropdown, sync to idx
    st.session_state[idx_key] = selected

# --- Navigation buttons ---
c1, c2 = st.columns([1, 1])
with c1:
    st.button("◀ Previous", use_container_width=True, key="prev_btn", on_click=go_prev)
with c2:
    st.button("Next ▶", use_container_width=True, key="next_btn", on_click=go_next)

# --- Display ---
idx = st.session_state[idx_key]
st.markdown(f"**{chapter}** · Slide **{idx} / {n}**")

url = slide_url(folder, idx, prefix, ext)
st.image(url, use_container_width=True)
