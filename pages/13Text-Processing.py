import streamlit as st
import re
import pandas as pd
import io

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
    st.caption("Paste text below to see word frequency counts (case-insensitive). You can download the table as an Excel file.")

    text_for_freq = st.text_area("Paste your text here:", height=260, key="freq_text")

    c1, c2 = st.columns([1, 1])
    with c1:
        top_n = st.number_input("Show top N words (0 = show all)", min_value=0, max_value=5000, value=200, step=50)
    with c2:
        min_count = st.number_input("Minimum frequency (filter)", min_value=1, max_value=9999, value=1, step=1)

    if text_for_freq.strip():
        df_freq = word_frequency_df(text_for_freq, top_n=None if top_n == 0 else int(top_n))

        # Apply minimum count filter
        df_freq = df_freq[df_freq["count"] >= int(min_count)].reset_index(drop=True)

        if df_freq.empty:
            st.warning("No tokens found (or all filtered out).")
        else:
            st.write(f"✅ Unique words: **{len(df_freq)}**")
            st.dataframe(df_freq, use_container_width=True, hide_index=True)

            # Excel download
            excel_bytes = df_to_excel_bytes(df_freq)
            st.download_button(
                label="⬇️ Download Excel (.xlsx)",
                data=excel_bytes,
                file_name="word_frequency.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_freq_xlsx",
            )
    else:
        st.info("Paste some text to generate the frequency table.")

# ---- Tab 4 ----
with tabs[3]:
    st.header("Application 4")
    st.write("Details for Application 4 will be added here.")

# ---- Tab 5 ----
with tabs[4]:
    st.header("Application 5")
    st.write("Details for Application 5 will be added here.")
