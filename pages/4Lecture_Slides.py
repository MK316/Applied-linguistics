import streamlit as st

# =========================
# Config (edit only this)
# =========================
RAW_BASE = "https://raw.githubusercontent.com/MK316/Applied-linguistics/main"

# Assumption: slide_001.png, slide_002.png, ... (3-digit)
SLIDE_SETS = {
    "Ch 1": {"folder": "lectureslides/test", "n": 2, "prefix": "slide_", "ext": "png"},
    "Ch 2": {"folder": "lectureslides/ch02", "n": 18, "prefix": "slide_", "ext": "png"},
    "Ch 3": {"folder": "lectureslides/ch03", "n": 30, "prefix": "slide_", "ext": "png"},
}

# =========================
# Helpers
# =========================
def slide_url(folder: str, idx_1based: int, prefix: str, ext: str) -> str:
    fname = f"{prefix}{idx_1based:03d}.{ext}"
    return f"{RAW_BASE}/{folder}/{fname}"

def init_state(key: str, default: int = 1):
    if key not in st.session_state:
        st.session_state[key] = default

def clamp(x: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, x))

def go_prev(state_key: str, n: int):
    st.session_state[state_key] = clamp(st.session_state[state_key] - 1, 1, n)

def go_next(state_key: str, n: int):
    st.session_state[state_key] = clamp(st.session_state[state_key] + 1, 1, n)

def set_from_select(state_key: str, n: int, select_key: str):
    st.session_state[state_key] = clamp(int(st.session_state[select_key]), 1, n)

# =========================
# UI
# =========================
st.markdown("#### Applied Linguistics (Spring 2026)")
st.caption("Slide viewer (GitHub-hosted images)")

tab_labels = list(SLIDE_SETS.keys())
tabs = st.tabs(tab_labels)

for tab, label in zip(tabs, tab_labels):
    cfg = SLIDE_SETS[label]
    folder, n, prefix, ext = cfg["folder"], int(cfg["n"]), cfg["prefix"], cfg["ext"]

    # Separate state per tab
    state_key = f"slide_idx__{label}"
    init_state(state_key, default=1)

    with tab:
        # --- Controls row (no Jump-to, no folder text) ---
        c1, c2, c3 = st.columns([1.1, 1.1, 3.2])

        with c1:
            st.button("◀ Previous", use_container_width=True, on_click=go_prev, args=(state_key, n))
        with c2:
            st.button("Next ▶", use_container_width=True, on_click=go_next, args=(state_key, n))

        with c3:
            slide_options = list(range(1, n + 1))
            select_key = f"select_slide__{label}"
            st.selectbox(
                "Select slide",
                options=slide_options,
                index=int(st.session_state[state_key]) - 1,
                key=select_key,
                on_change=set_from_select,
                args=(state_key, n, select_key),
            )

        # --- Display ---
        idx = int(st.session_state[state_key])
        url = slide_url(folder, idx, prefix, ext)

        st.markdown(f"**{label}** · Slide **{idx} / {n}**")
        st.image(url, use_container_width=True)

        # Optional debug (remove if you want it even cleaner)
        with st.expander("Troubleshoot (raw URL)"):
            st.code(url, language="text")
            st.caption("If this URL does not open in a browser, the path/filename is wrong.")
