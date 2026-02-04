import io
import requests
import pandas as pd
import streamlit as st



st.set_page_config(page_title="Phonetics Flashcards", layout="wide")

# =========================
# 1) Put your GitHub RAW CSV URLs here
# =========================
CHAPTERS = {
    "Chapter 1": "https://raw.githubusercontent.com/MK316/Applied-linguistics/refs/heads/main/data/CH01_flashcards.csv",
    "Chapter 2": "https://raw.githubusercontent.com/YOURNAME/YOURREPO/main/data/ch02.csv",
    "Chapter 3": "https://raw.githubusercontent.com/YOURNAME/YOURREPO/main/data/ch03.csv",
    "Chapter 4": "https://raw.githubusercontent.com/YOURNAME/YOURREPO/main/data/ch04.csv",
    "Chapter 5": "https://raw.githubusercontent.com/YOURNAME/YOURREPO/main/data/ch05.csv",
}

# =========================
# 2) Helpers
# =========================
def _norm_cols(df: pd.DataFrame) -> dict:
    """Map lowercase column names -> original names."""
    return {c.lower().strip(): c for c in df.columns}

def pick_qa_columns(df: pd.DataFrame) -> tuple[str, str]:
    """
    Try to auto-detect question/answer columns.
    Accepts: question/answer, q/a, front/back, term/definition, prompt/response
    """
    m = _norm_cols(df)

    q_candidates = ["question", "q", "front", "term", "prompt"]
    a_candidates = ["answer", "a", "back", "definition", "response"]

    q_col = next((m[k] for k in q_candidates if k in m), None)
    a_col = next((m[k] for k in a_candidates if k in m), None)

    if q_col and a_col:
        return q_col, a_col

    # Fallback: first two columns
    if df.shape[1] >= 2:
        return df.columns[0], df.columns[1]

    raise ValueError("CSV must have at least 2 columns for (question, answer).")

@st.cache_data(ttl=3600, show_spinner=False)
def load_cards(csv_url: str) -> pd.DataFrame:
    headers = {
        "User-Agent": "Mozilla/5.0"   # ✅ sometimes helps with github raw
    }

    # Optional: private repo token
    token = st.secrets.get("GITHUB_TOKEN", None)
    if token:
        headers["Authorization"] = f"token {token}"

    r = requests.get(csv_url, headers=headers, timeout=20)

    if r.status_code != 200:
        # ✅ streamlit will show the reason
        raise RuntimeError(
            f"Failed to load CSV.\nURL: {csv_url}\nHTTP {r.status_code}: {r.text[:200]}"
        )

    return pd.read_csv(io.BytesIO(r.content))

def clamp(x: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, x))

def cb_prev(ch_key: str):
    st.session_state[f"{ch_key}__idx"] = clamp(st.session_state[f"{ch_key}__idx"] - 1, 0, st.session_state[f"{ch_key}__n"] - 1)
    st.session_state[f"{ch_key}__show"] = False

def cb_next(ch_key: str):
    st.session_state[f"{ch_key}__idx"] = clamp(st.session_state[f"{ch_key}__idx"] + 1, 0, st.session_state[f"{ch_key}__n"] - 1)
    st.session_state[f"{ch_key}__show"] = False

def cb_shuffle(ch_key: str, df: pd.DataFrame, n: int):
    order = list(range(len(df)))
    random.shuffle(order)
    st.session_state[f"{ch_key}__order"] = order[:n]
    st.session_state[f"{ch_key}__idx"] = 0
    st.session_state[f"{ch_key}__show"] = False
    st.session_state[f"{ch_key}__n"] = n

def init_state(ch_key: str, df: pd.DataFrame):
    # init defaults once
    if f"{ch_key}__order" not in st.session_state:
        order = list(range(len(df)))
        random.shuffle(order)
        st.session_state[f"{ch_key}__order"] = order
    if f"{ch_key}__idx" not in st.session_state:
        st.session_state[f"{ch_key}__idx"] = 0
    if f"{ch_key}__show" not in st.session_state:
        st.session_state[f"{ch_key}__show"] = False
    if f"{ch_key}__n" not in st.session_state:
        st.session_state[f"{ch_key}__n"] = min(10, len(df)) if len(df) else 0

# =========================
# 3) UI styles (flashcard look)
# =========================
st.markdown(
    """
    <style>
      .card-wrap{
        width: 100%;
        display:flex;
        justify-content:center;
        margin-top: 8px;
        margin-bottom: 8px;
      }
      .flashcard{
        width: min(520px, 95%);
        min-height: 360px;
        background: #2f3133;
        border-radius: 28px;
        padding: 36px 34px;
        box-shadow: 0 10px 28px rgba(0,0,0,0.18);
        display:flex;
        flex-direction:column;
        justify-content:center;
        gap: 18px;
      }
      .qtext{
        color: #ffffff;
        font-size: 30px;
        line-height: 1.35;
        font-weight: 700;
        text-align:left;
        word-break: break-word;
      }
      .subtle{
        color: rgba(255,255,255,0.65);
        font-size: 14px;
        margin-top: 10px;
        text-align:center;
      }
      .answer-box{
        width: min(520px, 95%);
        margin: 0 auto;
        padding: 14px 16px;
        border-radius: 14px;
        background: rgba(0,0,0,0.03);
        border: 1px solid rgba(0,0,0,0.06);
      }
      .answer-title{
        font-weight: 700;
        margin-bottom: 6px;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# 4) App layout
# =========================
st.title("Phonetics Flashcards")
st.caption("Flashcards from GitHub CSV · Select a chapter tab, choose how many cards to practice, then navigate.")

tabs = st.tabs(list(CHAPTERS.keys()))

for tab, (chapter_name, csv_url) in zip(tabs, CHAPTERS.items()):
    ch_key = chapter_name.replace(" ", "_").lower()

    with tab:
        st.subheader(chapter_name)

        try:
            df = load_cards(csv_url)
        except Exception as e:
            st.error(str(e))
            st.stop()


        if df is None or df.empty:
            st.error("No cards found. Please check the CSV URL and file contents.")
            st.caption("Expected columns: question/answer (or Q/A, Front/Back, Term/Definition).")
            st.code(csv_url, language="text")
            continue

        init_state(ch_key, df)

        total = len(df)

        # ---- Controls row ----
        c1, c2, c3, c4 = st.columns([1.4, 1.2, 1.4, 2.0], vertical_alignment="bottom")

        with c1:
            n_pick = st.slider(
                "Number of cards",
                min_value=5,
                max_value=(total if total >= 5 else total),
                value=clamp(st.session_state[f"{ch_key}__n"], 5, total) if total >= 5 else total,
                step=5 if total >= 10 else 1,
                key=f"{ch_key}__slider_n",
                help="Choose how many items to practice (step = 5).",
            )

        with c2:
            shuffle_now = st.button("🔀 Shuffle", use_container_width=True, key=f"{ch_key}__btn_shuffle")
        with c3:
            reset_now = st.button("↺ Restart", use_container_width=True, key=f"{ch_key}__btn_restart")
        with c4:
            st.caption("Source (RAW URL)")
            st.code(csv_url, language="text")

        # Apply shuffle / reset
        if shuffle_now or reset_now:
            cb_shuffle(ch_key, df, int(n_pick))

        # Keep n in state (if slider changed)
        st.session_state[f"{ch_key}__n"] = int(n_pick)

        # Ensure order length >= n
        order = st.session_state[f"{ch_key}__order"]
        if len(order) < total:
            # if somehow shorter, rebuild
            order = list(range(total))
            random.shuffle(order)
        order = order[: int(n_pick)]
        st.session_state[f"{ch_key}__order"] = order

        n = len(order)
        if n == 0:
            st.warning("Not enough items to display.")
            continue

        # Clamp idx
        st.session_state[f"{ch_key}__idx"] = clamp(st.session_state[f"{ch_key}__idx"], 0, n - 1)
        idx = st.session_state[f"{ch_key}__idx"]
        row = df.iloc[order[idx]]
        question = row["question"]
        answer = row["answer"]

        # ---- Navigation row (Prev / Next) + progress ----
        nav1, nav2, nav3 = st.columns([1.2, 2.6, 1.2], vertical_alignment="center")
        with nav1:
            st.button(
                "◀",
                key=f"{ch_key}__prev",
                use_container_width=True,
                on_click=cb_prev,
                args=(ch_key,),
                disabled=(idx == 0),
            )
        with nav2:
            st.markdown(f"**{idx + 1} / {n} cards**")
            st.progress((idx + 1) / n)
        with nav3:
            st.button(
                "▶",
                key=f"{ch_key}__next",
                use_container_width=True,
                on_click=cb_next,
                args=(ch_key,),
                disabled=(idx == n - 1),
            )

        # ---- Flashcard ----
        st.markdown(
            f"""
            <div class="card-wrap">
              <div class="flashcard">
                <div class="qtext">{question}</div>
                <div class="subtle">Use “Show answer” below</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ---- Show answer section ----
        show_label = "Show answer"
        show = st.toggle(show_label, value=st.session_state[f"{ch_key}__show"], key=f"{ch_key}__toggle_show")
        st.session_state[f"{ch_key}__show"] = show

        if show:
            st.markdown(
                f"""
                <div class="answer-box">
                  <div class="answer-title">Answer</div>
                  <div>{answer}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
