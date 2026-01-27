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
def slide_url(folder, idx, prefix, ext):
    return f"{RAW_BASE}/{folder}/{prefix}{idx:03d}.{ext}"

def init_state(key, default=1):
    if key not in st.session_state:
        st.session_state[key] = default

def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def go_prev(state_key, n):
    st.session_state[state_key] = clamp(st.session_state[state_key] - 1, 1, n)

def go_next(state_key, n):
    st.session_state[state_key] = clamp(st.session_state[state_key] + 1, 1, n)

# =========================
# UI
# =========================
st.markdown("#### Applied Linguistics (Spring 2026)")
st.caption("Lecture slide viewer")

tab_labels = list(SLIDE_SETS.keys())
tabs = st.tabs(tab_labels)

for tab, label in zip(tabs, tab_labels):
    cfg = SLIDE_SETS[label]
    folder, n, prefix, ext = cfg["folder"], cfg["n"], cfg["prefix"], cfg["ext"]

    state_key = f"slide_idx__{label}"
    init_state(state_key)

    # ---- Sidebar: slide selector (per chapter) ----
    with st.sidebar:
        st.markdown(f"### {label}")
        selected = st.selectbox(
            "Select slide",
            options=list(range(1, n + 1)),
            index=st.session_state[state_key] - 1,
            key=f"sidebar_select__{label}",
        )
        st.session_state[state_key] = selected

    with tab:
        # ---- Navigation buttons ----
        c1, c2 = st.columns([1, 1])

        with c1:
            st.button(
                "◀ Previous",
                use_container_width=True,
                key=f"prev__{label}",
                on_click=go_prev,
                args=(state_key, n),
            )

        with c2:
            st.button(
                "Next ▶",
                use_container_width=True,
                key=f"next__{label}",
                on_click=go_next,
                args=(state_key, n),
            )

        # ---- Display slide ----
        idx = st.session_state[state_key]
        url = slide_url(folder, idx, prefix, ext)

        st.markdown(f"**{label}** · Slide **{idx} / {n}**")
        st.image(url, use_container_width=True)
