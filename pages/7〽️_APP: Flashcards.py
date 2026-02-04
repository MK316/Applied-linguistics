import streamlit as st
import pandas as pd
import random
import io
import requests

# 1. 설정 및 상수
st.set_page_config(page_title="Phonetics Flashcards", layout="wide")

CHAPTERS = {
    "Chapter 1": "https://raw.githubusercontent.com/MK316/Applied-linguistics/refs/heads/main/data/CH01_flashcards.csv",
    "Chapter 2": "https://raw.githubusercontent.com/YOURNAME/YOURREPO/main/data/ch02.csv",
    "Chapter 3": "https://raw.githubusercontent.com/YOURNAME/YOURREPO/main/data/ch03.csv",
    "Chapter 4": "https://raw.githubusercontent.com/YOURNAME/YOURREPO/main/data/ch04.csv",
    "Chapter 5": "https://raw.githubusercontent.com/YOURNAME/YOURREPO/main/data/ch05.csv",
}

# 2. 헬퍼 함수
def pick_qa_columns(df: pd.DataFrame) -> tuple[str, str]:
    cols = {c.lower().strip(): c for c in df.columns}
    q_candidates = ["question", "q", "front", "term", "prompt"]
    a_candidates = ["answer", "a", "back", "definition", "response"]

    q_col = next((cols[k] for k in q_candidates if k in cols), None)
    a_col = next((cols[k] for k in a_candidates if k in cols), None)

    if not q_col or not a_col:
        if df.shape[1] < 2:
            raise ValueError(f"CSV needs at least 2 columns. Found: {list(df.columns)}")
        q_col, a_col = df.columns[0], df.columns[1]
    return q_col, a_col

@st.cache_data(ttl=3600, show_spinner="Loading data...")
def load_cards(csv_url: str) -> pd.DataFrame:
    headers = {"User-Agent": "Mozilla/5.0"}
    token = st.secrets.get("GITHUB_TOKEN", None)
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        r = requests.get(csv_url, headers=headers, timeout=10)
        r.raise_for_status()
        df = pd.read_csv(io.BytesIO(r.content))
    except Exception as e:
        # 에러 발생 시 빈 데이터프레임 반환 혹은 에러 전파
        return pd.DataFrame()

    if df.empty:
        return df

    q_col, a_col = pick_qa_columns(df)
    out = df[[q_col, a_col]].copy()
    out.columns = ["question", "answer"]
    out["question"] = out["question"].astype(str).str.strip()
    out["answer"] = out["answer"].astype(str).str.strip()
    out = out[(out["question"] != "") & (out["answer"] != "")]
    return out.reset_index(drop=True)

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
    st.session_state[f"{ch_key}__order"] = order
    st.session_state[f"{ch_key}__idx"] = 0
    st.session_state[f"{ch_key}__show"] = False
    st.session_state[f"{ch_key}__n"] = n

def init_state(ch_key: str, df: pd.DataFrame):
    if f"{ch_key}__order" not in st.session_state:
        order = list(range(len(df)))
        random.shuffle(order)
        st.session_state[f"{ch_key}__order"] = order
    if f"{ch_key}__idx" not in st.session_state:
        st.session_state[f"{ch_key}__idx"] = 0
    if f"{ch_key}__show" not in st.session_state:
        st.session_state[f"{ch_key}__show"] = False
    if f"{ch_key}__n" not in st.session_state:
        st.session_state[f"{ch_key}__n"] = min(10, len(df))

# 3. CSS 스타일
st.markdown("""
    <style>
      .card-wrap{ width: 100%; display:flex; justify-content:center; margin: 10px 0; }
      .flashcard{
        width: min(520px, 95%); min-height: 300px;
        background: #2f3133; border-radius: 28px; padding: 40px;
        box-shadow: 0 10px 28px rgba(0,0,0,0.2);
        display:flex; flex-direction:column; justify-content:center; align-items:center;
      }
      .qtext{ color: #ffffff; font-size: 28px; font-weight: 700; text-align:center; word-break: break-word; }
      .subtle{ color: rgba(255,255,255,0.5); font-size: 14px; margin-top: 20px; }
      .answer-box{
        width: min(520px, 95%); margin: 10px auto; padding: 20px;
        border-radius: 14px; background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
      }
      .answer-title{ font-weight: 700; color: #ff4b4b; margin-bottom: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 4. 앱 레이아웃
st.title("Phonetics Flashcards")
tabs = st.tabs(list(CHAPTERS.keys()))

for tab, (chapter_name, csv_url) in zip(tabs, CHAPTERS.items()):
    ch_key = chapter_name.replace(" ", "_").lower()

    with tab:
        st.subheader(chapter_name)
        
        # 순서 수정: df를 먼저 로드해야 함
        df = load_cards(csv_url)

        if df.empty:
            st.warning(f"No data found at {csv_url}. Please check the URL.")
            continue

        init_state(ch_key, df)
        total = len(df)

        # 컨트롤 영역
        c1, c2, c3, c4 = st.columns([1.5, 1, 1, 2], vertical_alignment="bottom")
        
        with c1:
            n_val = st.session_state[f"{ch_key}__n"]
            n_pick = st.slider(
                "Cards to practice",
                min_value=1, max_value=total,
                value=clamp(n_val, 1, total),
                key=f"{ch_key}__slider_n"
            )
        
        with c2:
            if st.button("🔀 Shuffle", key=f"{ch_key}__btn_shuf", use_container_width=True):
                cb_shuffle(ch_key, df, int(n_pick))
                st.rerun()
        
        with c3:
            if st.button("↺ Restart", key=f"{ch_key}__btn_res", use_container_width=True):
                st.session_state[f"{ch_key}__idx"] = 0
                st.session_state[f"{ch_key}__show"] = False
                st.rerun()

        # 데이터 로직
        order = st.session_state[f"{ch_key}__order"][:int(n_pick)]
        idx = clamp(st.session_state[f"{ch_key}__idx"], 0, len(order)-1)
        
        # 카드 표시
        row = df.iloc[order[idx]]
        
        nav1, nav2, nav3 = st.columns([1, 2, 1], vertical_alignment="center")
        with nav1:
            st.button("◀", key=f"{ch_key}__prev", on_click=cb_prev, args=(ch_key,), disabled=(idx==0), use_container_width=True)
        with nav2:
            st.markdown(f"<center><b>{idx + 1} / {len(order)}</b></center>", unsafe_allow_html=True)
            st.progress((idx + 1) / len(order))
        with nav3:
            st.button("▶", key=f"{ch_key}__next", on_click=cb_next, args=(ch_key,), disabled=(idx==len(order)-1), use_container_width=True)

        st.markdown(f"""
            <div class="card-wrap">
              <div class="flashcard">
                <div class="qtext">{row['question']}</div>
                <div class="subtle">Click 'Show Answer' to reveal</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        show = st.toggle("Show Answer", value=st.session_state[f"{ch_key}__show"], key=f"{ch_key}__toggle")
        st.session_state[f"{ch_key}__show"] = show

        if show:
            st.markdown(f"""
                <div class="answer-box">
                  <div class="answer-title">Answer</div>
                  <div>{row['answer']}</div>
                </div>
                """, unsafe_allow_html=True)
