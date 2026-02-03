import streamlit as st
import re
import pandas as pd
import io
import matplotlib.pyplot as plt
import math
import textstat



# ----------------------------
# Functions
# ----------------------------
def count_words(text: str) -> int:
    return len(re.findall(r"\w+", text))

def count_sentences(text: str) -> int:
    # ✅ fixed: no +1
    return len(re.findall(r"[.!?]+", text))

def remove_line_breaks(text: str) -> str:
    return re.sub(r"[\r\n]+", " ", text)

def word_frequency_df(text: str, top_n: int | None = None) -> pd.DataFrame:
    """
    - lowercases text for case-insensitive counts
    - counts word tokens (letters/digits/underscore via \w)
    - returns DataFrame sorted by frequency desc, then word asc
    """
    cleaned = text.lower()
    tokens = re.findall(r"\w+", cleaned)

    if not tokens:
        return pd.DataFrame(columns=["word", "count"])

    s = pd.Series(tokens, dtype="string")
    freq = s.value_counts().reset_index()
    freq.columns = ["word", "count"]
    freq = freq.sort_values(by=["count", "word"], ascending=[False, True], ignore_index=True)

    if top_n is not None:
        freq = freq.head(top_n)

    return freq

def df_to_excel_bytes(df: pd.DataFrame, sheet_name: str = "word_frequency") -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    output.seek(0)
    return output.getvalue()

def tokenize_words(text: str):
    """
    교육용 기본 토큰화:
    - 알파벳 단어 + 아포스트로피 포함 (don't, teacher's)
    - 모두 소문자로 정규화
    """
    return re.findall(r"[a-zA-Z]+(?:'[a-zA-Z]+)?", text.lower())

# ----------------------------
# Streamlit UI
# ----------------------------
st.title("Text Processing Tools")

tabs = st.tabs(["Word Count", "Remove Line Breaks", "Word Frequency", "Application 4", "Application 5"])

# ---- Tab 1: Word Count ----
with tabs[0]:
    st.header("🔍 Word and Sentence Counter")
    st.caption(
        "This application will display the number of words and sentences in your text. "
        "After pasting your text in the box below, hit 'Control + Enter' key to see the result."
    )
    user_input = st.text_area("Paste your text here:", height=300, key="wc_text")

    if user_input:
        word_count = count_words(user_input)
        sentence_count = count_sentences(user_input)
        st.write("✏️ Here's the text count summary:")
        st.write(f"〽️ **Word Count**: {word_count}")
        st.write(f"〽️ **Sentence Count**: {sentence_count}")

# ---- Tab 2: Remove Line Breaks ----
with tabs[1]:
    st.header("🔄 Remove Line Breaks")
    st.caption("Paste your text here and see it transformed without line breaks, making it easier to copy without formatting.")
    user_input = st.text_area("Paste your text here to remove line breaks:", height=300, key="rlb_text")

    if user_input:
        processed_text = remove_line_breaks(user_input)
        st.write("📝 Here's your text without line breaks:")
        st.text_area("Copy the text below:", processed_text, height=300, key="processed")

# ---- Tab 3: Word Frequency (NEW) ----
with tabs[2]:
    st.header("📊 Word Frequency")
    st.caption(
        "Paste text to see word frequency (case-insensitive). "
        "You can provide stop words separated by commas. "
        "You can also draw a bar chart for the most frequent words."
    )

    text_for_freq = st.text_area(
        "Paste your text here:",
        height=220,
        key="freq_text",
    )

    stop_words_input = st.text_input(
        "Stop words (comma-separated, optional)",
        placeholder="e.g., the, a, an, and, of, to",
        key="stop_words_input",
    )

    c1, c2 = st.columns([1, 1])
    with c1:
        top_n_table = st.number_input(
            "Show top N words in table (0 = show all)",
            min_value=0,
            max_value=5000,
            value=200,
            step=50,
            key="top_n_table",
        )
    with c2:
        min_count = st.number_input(
            "Minimum frequency (filter)",
            min_value=1,
            max_value=9999,
            value=1,
            step=1,
            key="min_count",
        )

    # ---- Build frequency table once (used by both table + chart) ----
    df_freq = pd.DataFrame(columns=["word", "count"])

    if text_for_freq.strip():
        text_lower = text_for_freq.lower()
        tokens = re.findall(r"\w+", text_lower)

        # Parse stop words
        stop_words = set()
        if stop_words_input.strip():
            stop_words = {
                w.strip().lower()
                for w in stop_words_input.split(",")
                if w.strip()
            }

        # Remove stop words
        if stop_words:
            tokens = [t for t in tokens if t not in stop_words]

        if not tokens:
            st.warning("No tokens left after applying stop words.")
        else:
            s = pd.Series(tokens, dtype="string")
            df_freq = s.value_counts().reset_index()
            df_freq.columns = ["word", "count"]
            df_freq = df_freq.sort_values(
                by=["count", "word"],
                ascending=[False, True],
                ignore_index=True,
            )

            # Apply min_count first (so both table and chart reflect it)
            df_freq = df_freq[df_freq["count"] >= int(min_count)].reset_index(drop=True)

            if df_freq.empty:
                st.warning("All words were filtered out by the minimum frequency setting.")
            else:
                # ---- Table (optionally top N) ----
                df_table = df_freq if top_n_table == 0 else df_freq.head(int(top_n_table))

                st.write(f"✅ Unique words (after filters): **{len(df_freq)}**")
                st.dataframe(df_table, use_container_width=True, hide_index=True)

                # ---- CSV download (table content you see) ----
                csv_data = df_table.to_csv(index=False).encode("utf-8-sig")
                st.download_button(
                    label="⬇️ Download CSV (table)",
                    data=csv_data,
                    file_name="word_frequency.csv",
                    mime="text/csv",
                    key="download_freq_csv",
                )

                st.markdown("---")

                # ---- Chart controls (button -> reveal options) ----
                if "show_chart_opts" not in st.session_state:
                    st.session_state["show_chart_opts"] = False

                if st.button("📊 Show chart options", key="toggle_chart_opts"):
                    st.session_state["show_chart_opts"] = not st.session_state["show_chart_opts"]

                if st.session_state["show_chart_opts"]:
                    st.subheader("Bar chart")

                    chart_top_n = st.slider(
                        "Top N for chart",
                        min_value=5,
                        max_value=min(50, len(df_freq)),
                        value=min(20, len(df_freq)),
                        step=1,
                        key="chart_top_n",
                    )

                    if st.button("Draw bar chart", key="draw_bar_chart"):
                        plot_df = df_freq.head(int(chart_top_n)).copy()

                        # Make y labels readable (shorten if extremely long)
                        plot_df["word"] = plot_df["word"].astype(str).str.slice(0, 35)

                        fig, ax = plt.subplots(figsize=(10, max(4, 0.35 * len(plot_df))))
                        ax.barh(plot_df["word"][::-1], plot_df["count"][::-1])
                        ax.set_xlabel("Frequency")
                        ax.set_ylabel("Word")
                        ax.set_title(f"Top {chart_top_n} Words by Frequency")
                        plt.tight_layout()

                        st.pyplot(fig)

    else:
        st.info("Paste some text to generate the frequency table.")

# ---- Tab 4 ----


with tabs[3]:
    st.header("📚 Token–Type Statistics (TTS) + Lexical Diversity")
    st.caption("Paste text to compute token/type counts and common lexical diversity indices (case-insensitive).")

    text = st.text_area("Paste your text here:", height=260, key="tts_text")

    stop_words_input = st.text_input(
        "Stop words (comma-separated, optional)",
        placeholder="e.g., the, a, an, and, of, to",
        key="tts_stopwords",
    )

    c1, c2 = st.columns([1, 1])
    with c1:
        min_count = st.number_input("Minimum frequency (optional filter)", 1, 9999, 1, 1, key="tts_min_count")
    with c2:
        show_top = st.slider("Show top frequent words", 5, 50, 20, 5, key="tts_topn")

    if text.strip():
        # ---- stop words parse (case-insensitive) ----
        stop_words = set()
        if stop_words_input.strip():
            stop_words = {w.strip().lower() for w in stop_words_input.split(",") if w.strip()}

        # ---- tokenize ----
        tokens = tokenize_words(text)

        # ---- remove stop words ----
        if stop_words:
            tokens = [t for t in tokens if t not in stop_words]

        if not tokens:
            st.warning("No tokens found (or all tokens removed by stop words).")
        else:
            # ---- frequency table ----
            freq = pd.Series(tokens).value_counts().reset_index()
            freq.columns = ["word", "count"]

            # optional filter by min_count
            freq = freq[freq["count"] >= int(min_count)].reset_index(drop=True)

            if freq.empty:
                st.warning("All tokens were filtered out by the minimum frequency setting.")
            else:
                # reconstruct filtered token list (so TTS indices match filtering)
                # (교육용이라 'min_count 필터' 적용 시 지표도 그 기준으로 맞추는 방식)
                filtered_tokens = []
                for _, row in freq.iterrows():
                    filtered_tokens.extend([row["word"]] * int(row["count"]))

                N = len(filtered_tokens)                 # tokens
                V = int(freq.shape[0])                   # types

                # ---- common lexical diversity indices ----
                ttr = V / N
                root_ttr = V / math.sqrt(N)              # Guiraud
                cttr = V / math.sqrt(2 * N)              # corrected TTR
                log_ttr = (math.log(V) / math.log(N)) if (V > 1 and N > 1) else float("nan")

                # ---- summary table ----
                summary = pd.DataFrame(
                    [
                        ["Tokens (N)", N],
                        ["Types (V)", V],
                        ["TTR = V/N", round(ttr, 4)],
                        ["Root TTR (Guiraud) = V/√N", round(root_ttr, 4)],
                        ["CTTR = V/√(2N)", round(cttr, 4)],
                        ["Log TTR = log(V)/log(N)", "" if math.isnan(log_ttr) else round(log_ttr, 4)],
                    ],
                    columns=["Metric", "Value"],
                )

                st.subheader("✅ Token–Type Summary")
                st.dataframe(summary, use_container_width=True, hide_index=True)

                st.subheader("📌 Top word frequencies")
                st.dataframe(freq.head(int(show_top)), use_container_width=True, hide_index=True)

    else:
        st.info("Paste text to compute token–type statistics.")


# ---- Tab 5 ----
with tabs[4]:
    st.header("📚 Reading Level & Lexical Analyzer")
    st.markdown("""
    This app estimates the complexity of your text using standard readability formulas.  
    Since the official **Lexile®** formula is proprietary, this tool uses  
    **Flesch–Kincaid** and **Text Standard** scores as educational proxies.
    """)

    # Input Section
    text_input = st.text_area(
        "Paste your text here (minimum 100 words recommended):",
        height=300,
        key="lexile_text_input",
    )

    if text_input.strip():
        # ----------------------------
        # Core counts
        # ----------------------------
        word_count = textstat.lexicon_count(text_input, removepunct=True)
        sentence_count = textstat.sentence_count(text_input)

        # ----------------------------
        # Readability metrics
        # ----------------------------
        fk_grade = textstat.flesch_kincaid_grade(text_input)
        consensus_grade = textstat.text_standard(text_input)

        # ----------------------------
        # Lexical Diversity (simple TTR)
        # ----------------------------
        words = re.findall(r"[a-zA-Z]+(?:'[a-zA-Z]+)?", text_input.lower())
        unique_words = set(words)
        ttr = len(unique_words) / len(words) if words else 0

        # ----------------------------
        # Display Metrics
        # ----------------------------
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Grade Level", f"Grade {fk_grade}")
            st.caption("Flesch–Kincaid Estimate")

        with col2:
            st.metric("Lexical Diversity", f"{ttr:.2f}")
            st.caption("Type–Token Ratio (TTR)")

        with col3:
            st.metric("Word Count", word_count)

        st.divider()

        # ----------------------------
        # Interpretation
        # ----------------------------
        st.subheader("📝 Analysis Summary")
        st.write(f"**Recommended Audience:** {consensus_grade}")

        # Lexile proxy (heuristic)
        lexile_proxy = int((fk_grade * 150) + 150) if fk_grade > 0 else 0
        st.info(
            f"**Estimated Lexile Range:** "
            f"{max(0, lexile_proxy - 50)}L – {lexile_proxy + 50}L"
        )

        # Visual indicator
        st.progress(
            min(fk_grade / 12.0, 1.0),
            text=f"Text Complexity (relative): {fk_grade} / 12",
        )

    else:
        st.info("Waiting for text input…")

