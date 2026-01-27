import streamlit as st

# =========================
# Config (edit only this)
# =========================
RAW_BASE = "https://raw.githubusercontent.com/MK316/Applied-linguistics/main"

# Each tab points to a different GitHub folder + slide count.
# Assumption: images are named slide_001.png, slide_002.png, ... (3-digit)
SLIDE_SETS = {
    "Ch 1": {"folder": "lectureslides/test", "n": 2, "prefix": "test.", "ext": "png"}
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

def jump_to(state_key: str, n: int, value: int):
    st.session_state[state_key] = clamp(int(value), 1, n)

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
        # --- Controls row ---
        c1, c2, c3, c4, c5 = st.columns([1.1, 1.1, 2.2, 2.2, 2.2])

        with c1:
            st.button("◀ Previous", use_container_width=True, on_click=go_prev, args=(state_key, n))
        with c2:
            st.button("Next ▶", use_container_width=True, on_click=go_next, args=(state_key, n))

        with c3:
            # Jump by number
            jump_num = st.number_input(
                "Jump to slide #",
                min_value=1,
                max_value=n,
                value=int(st.session_state[state_key]),
                step=1,
                key=f"jump_num__{label}",
                on_change=lambda: jump_to(state_key, n, st.session_state[f"jump_num__{label}"]),
            )

        with c4:
            # Jump by dropdown (optional but convenient)
            slide_options = list(range(1, n + 1))
            st.selectbox(
                "Select slide",
                options=slide_options,
                index=int(st.session_state[state_key]) - 1,
                key=f"jump_select__{label}",
                on_change=lambda: jump_to(state_key, n, st.session_state[f"jump_select__{label}"]),
            )

        with c5:
            st.write("")  # spacing
            st.caption(f"Folder: `{folder}`")

        # --- Display ---
        idx = int(st.session_state[state_key])
        url = slide_url(folder, idx, prefix, ext)

        st.markdown(f"**{label}** · Slide **{idx} / {n}**")
        st.image(url, use_container_width=True)

        # Optional: direct link for debugging (helps when a file is missing)
        with st.expander("Troubleshoot (raw URL)"):
            st.code(url, language="text")
            st.caption("If this URL does not open in a browser, the path/filename is wrong.")

"""
How to add more tabs later:
- Add a new entry to SLIDE_SETS with folder + n (and naming pattern if needed).

Naming requirement:
- slide_001.png ... slide_0NN.png inside each folder.
"""

