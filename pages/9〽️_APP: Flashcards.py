import streamlit as st
import pandas as pd
import random
import io
import requests

# 1. 앱 설정
st.set_page_config(page_title="Phonetics Flashcards", layout="wide")

CHAPTERS = {
    "Chapter 1": "https://raw.githubusercontent.com/MK316/Applied-linguistics/refs/heads/main/data/CH01_flashcards.csv",
    "Chapter 2": "https://raw.githubusercontent.com/YOURNAME/YOURREPO/main/data/ch02.csv",
    "Chapter 3": "https://raw.githubusercontent.com/YOURNAME/YOURREPO/main/data/ch03.csv",
    "Chapter 4": "https://raw.githubusercontent.com/YOURNAME/YOURREPO/main/data/ch04.csv",
    "Chapter 5": "https://raw.githubusercontent.com/YOURNAME/YOURREPO/main/data/ch05.csv",
}

# 2. 로직 함수들
@st.cache_data(ttl=3600, show_spinner="Loading data...")
def load_cards(csv_url: str) -> pd.DataFrame:
    try:
        r = requests.get(csv_url, timeout=10)
        r.raise_for_status()
        df = pd.read_csv(io.BytesIO(r.content))
        
        # 컬럼 표준화 (질문/답변 찾기)
        cols = {c.lower().strip(): c for c in df.columns}
        q_col = next((cols[k] for k in ["question", "q", "front", "term"] if k in cols), df.columns[0])
        a_col = next((cols[k] for k in ["answer", "a", "back", "definition"] if k in cols), df.columns[1])
        
        out = df[[q_col, a_col]].copy()
        out.columns = ["question", "answer"]
        return out.dropna().reset_index(drop=True)
    except:
        return pd.DataFrame()

def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def init_state(ch_key, total):
    if f"{ch_key}__order" not in st.session_state:
        order = list(range(total))
        random.shuffle(order)
        st.session_state[f"{ch_key}__order"] = order
    if f"{ch_key}__idx" not in st.session_state:
        st.session_state[f"{ch_key}__idx"] = 0
    if f"{ch_key}__n" not in st.session_state:
        st.session_state[f"{ch_key}__n"] = min(10, total)

# 3. CSS 스타일
st.markdown("""
    <style>
      .card-wrap { display: flex; justify-content: center; padding: 20px 0; }
      .flashcard {
        width: min(600px, 100%); min-height: 350px;
        background: #003366; border-radius: 30px; padding: 50px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        border: 1px solid #444;
      }
      .qtext { color: #ffffff; font-size: 32px; font-weight: 700; text-align: center; }
      .answer-box {
        width: min(600px, 100%); margin: 20px auto; padding: 25px;
        border-radius: 20px; background: #606060;
        border-left: 5px solid #FF9933; color: #ffffff; font-size: 18px;
      }
      .answer-title { font-weight: bold; color: #CCE5FF; margin-bottom: 10px; text-transform: uppercase; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# 4. 메인 화면 구성
st.title("🗂️ Phonetics Flashcards")

tabs = st.tabs(list(CHAPTERS.keys()))

for tab, (chapter_name, csv_url) in zip(tabs, CHAPTERS.items()):
    ch_key = chapter_name.replace(" ", "_").lower()
    
    with tab:
        df = load_cards(csv_url)
        if df.empty:
            st.error(f"Could not load data for {chapter_name}.")
            continue
            
        init_state(ch_key, len(df))
        
        # --- 사이드바 컨트롤 ---
        with st.sidebar:
            st.header(f"⚙️ {chapter_name} Settings")
            
            n_pick = st.slider(
                "Number of cards to practice",
                1, len(df), st.session_state[f"{ch_key}__n"],
                key=f"slider_{ch_key}"
            )
            st.session_state[f"{ch_key}__n"] = n_pick
            
            col_side1, col_side2 = st.columns(2)
            if col_side1.button("🔀 Shuffle", key=f"shuf_{ch_key}", use_container_width=True):
                new_order = list(range(len(df)))
                random.shuffle(new_order)
                st.session_state[f"{ch_key}__order"] = new_order
                st.session_state[f"{ch_key}__idx"] = 0
                st.rerun()
                
            if col_side2.button("↺ Reset", key=f"res_{ch_key}", use_container_width=True):
                st.session_state[f"{ch_key}__idx"] = 0
                st.rerun()

            st.divider()
            show_answer = st.toggle("🔓 Show Answer", key=f"show_{ch_key}")
            st.info("Tip: Use the sidebar to change settings without distracting your study.")

        # --- 메인 컨텐츠 ---
        order = st.session_state[f"{ch_key}__order"][:n_pick]
        current_idx = clamp(st.session_state[f"{ch_key}__idx"], 0, len(order) - 1)
        
        # 네비게이션 버튼 (메인 페이지 상단)
        nav1, nav2, nav3 = st.columns([1, 2, 1])
        with nav1:
            if st.button("◀ Prev", key=f"p_{ch_key}", disabled=(current_idx == 0), use_container_width=True):
                st.session_state[f"{ch_key}__idx"] -= 1
                st.rerun()
        with nav2:
            st.markdown(f"<h3 style='text-align: center;'>{current_idx + 1} / {len(order)}</h3>", unsafe_allow_html=True)
        with nav3:
            if st.button("Next ▶", key=f"n_{ch_key}", disabled=(current_idx == len(order) - 1), use_container_width=True):
                st.session_state[f"{ch_key}__idx"] += 1
                st.rerun()

        # 카드 렌더링
        card_data = df.iloc[order[current_idx]]
        st.markdown(f"""
            <div class="card-wrap">
              <div class="flashcard">
                <div class="qtext">{card_data['question']}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        # 정답 표시
        if show_answer:
            st.markdown(f"""
                <div class="answer-box">
                  <div class="answer-title">Correct Answer</div>
                  <div>{card_data['answer']}</div>
                </div>
                """, unsafe_allow_html=True)
