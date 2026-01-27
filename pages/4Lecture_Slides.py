import streamlit as st

st.set_page_config(layout="wide")  # ← MUST come first

#st.markdown("#### Applied Linguistics (Spring 2026)")
st.caption("Lecture slide viewer")



RAW_BASE = "https://raw.githubusercontent.com/MK316/Applied-linguistics/main"

SLIDE_SETS = {
    "Ch 1": {"folder": "lectureslides/test", "n": 2, "prefix": "test.", "ext": "png"},
    "Ch 2": {"folder": "lectureslides/ch02", "n": 18, "prefix": "slide_", "ext": "png"},
    "Ch 3": {"folder": "lectureslides/ch03", "n": 30, "prefix": "slide_", "ext": "png"},
}

def slide_url(folder: str, idx_1based: int, prefix: str, ext: str) -> str:
    return f"{RAW_BASE}/{folder}/{prefix}{idx_1based:03d}.{ext}"

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


tab_labels = list(SLIDE_SETS.keys())
tabs = st.tabs(tab_labels)

for tab, label in zip(tabs, tab_labels):
    cfg = SLIDE_SETS[label]
    folder, n, prefix, ext = cfg["folder"], int(cfg["n"]), cfg["prefix"], cfg["ext"]

    idx_key = f"idx__{label}"
    sel_key = f"sel__{label}"
    init_state(idx_key, 1)
    init_state(sel_key, st.session_state[idx_key])

    with tab:
        # ✅ Better alignment: hide label + add spacer
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
            # small spacer to match button baseline
            st.markdown("<div style='height: 2px;'></div>", unsafe_allow_html=True)

            st.selectbox(
                "Select slide",
                options=list(range(1, n + 1)),
                key=sel_key,
                index=st.session_state[idx_key] - 1,
                on_change=sync_from_select,
                args=(idx_key, sel_key),
                label_visibility="collapsed",  # ✅ removes label gap
            )

        idx = int(st.session_state[idx_key])
        url = slide_url(folder, idx, prefix, ext)  # ✅ define url here
        
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
