import streamlit as st
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="T-test Analyzer Fix", layout="wide")

if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False

st.title("📊 Step-by-Step T-test Analyzer")

# --- Sample Data Section ---
with st.expander("📝 테스트용 샘플 데이터 사용하기"):
    sample_link = "https://docs.google.com/spreadsheets/d/1k8SGYP7_SZDhDSdC4LVFl8rMsqdAUVHm3HK2HEClSDc/edit?usp=sharing"
    st.code(sample_link, language="text")

# --- Step 1: 데이터 로드 ---
st.header("1️⃣ Step: Load Data")
sheet_url = st.text_input("구글 시트 주소를 입력하세요:", 
                         placeholder="https://docs.google.com/spreadsheets/d/.../edit")

def get_google_sheet(url):
    try:
        file_id = url.split('/')[-2]
        raw_url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv"
        # 데이터 로드 시 공백 제거 및 타입 추론 방지 옵션 추가
        return pd.read_csv(raw_url, skipinitialspace=True)
    except: return None

if st.button("📥 데이터 불러오기"):
    if sheet_url:
        df_raw = get_google_sheet(sheet_url)
        if df_raw is not None:
            st.session_state.df = df_raw
            st.session_state.data_loaded = True
            st.session_state.analyzed = False # 새 데이터 로드 시 이전 결과 초기화
            st.success("데이터를 성공적으로 가져왔습니다!")
        else:
            st.error("URL을 확인해주세요. (시트 공유 권한 확인 필수)")

# --- Step 2: 변수 선택 및 검증 ---
if st.session_state.data_loaded:
    st.divider()
    st.header("2️⃣ Step: Select Variables & Descriptives")
    df = st.session_state.df.copy() # 원본 보존
    cols = df.columns.tolist()
    
    col1, col2 = st.columns(2)
    group_col = col1.selectbox("독립변수 (Group):", cols, index=0)
    value_col = col2.selectbox("종속변수 (Value):", cols, index=1 if len(cols)>1 else 0)
    
    # [데이터 인식 강화]
    # 1. 수치 열 강제 변환 및 결측치 제거
    df[value_col] = pd.to_numeric(df[value_col], errors='coerce')
    
    # 2. 분석에 사용할 깨끗한 데이터셋 생성
    clean_df = df.dropna(subset=[group_col, value_col])
    
    # 3. 감지된 집단 목록 확인
    detected_groups = sorted(clean_df[group_col].unique().tolist())
    
    # 현재 감지된 상태를 보여주는 디버깅 메시지
    st.write(f"🔍 **데이터 확인:** 현재 `{group_col}` 열에서 **{len(detected_groups)}개**의 집단이 감지되었습니다: `{detected_groups}`")

    if st.button("🔍 분석 실행"):
        if len(detected_groups) == 2:
            st.session_state.analyzed = True
            st.session_state.clean_df = clean_df
            st.session_state.groups = detected_groups
            st.session_state.group_col = group_col
            st.session_state.value_col = value_col
        else:
            st.error(f"T-test를 위해서는 집단이 정확히 2개여야 합니다. (현재 감지된 집단: {detected_groups})")
            st.info("💡 **해결 방법:** 구글 시트에서 집단 이름에 오타가 있거나, 데이터가 비어있지 않은지 확인해주세요.")

# --- Step 3: 결과 출력 ---
if st.session_state.analyzed:
    st.divider()
    df = st.session_state.clean_df
    groups = st.session_state.groups
    g_col = st.session_state.group_col
    v_col = st.session_state.value_col
    
    g1 = df[df[g_col] == groups[0]][v_col]
    g2 = df[df[g_col] == groups[1]][v_col]
    
    st.subheader("📋 Descriptive Statistics")
    desc = df.groupby(g_col)[v_col].agg(['count', 'mean', 'std']).reset_index()
    st.table(desc)

    t_stat, p_val = stats.ttest_ind(g1, g2)
    c1, c2, c3 = st.columns(3)
    c1.metric("T-value", f"{t_stat:.4f}")
    c2.metric("P-value", f"{p_val:.4f}")
    c3.metric("Result", "Significant" if p_val < 0.05 else "Not Significant")

    # 시각화 부분은 동일하게 유지하되 palette 에러 방지용 리스트 사용
    palette_options = ["Set2", "coolwarm", "viridis", "pastel"]
    palette = st.selectbox("색상 테마:", palette_options)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(x=g_col, y=v_col, data=df, palette=palette, ax=ax, hue=g_col, legend=False)
    st.pyplot(fig)
    
    if st.button("🔄 리셋하고 처음부터 하기"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
