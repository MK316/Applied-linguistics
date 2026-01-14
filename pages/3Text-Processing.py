import streamlit as st
import pandas as pd
import re
from collections import Counter
import string

# --------------------------
# Main App - Tab 1
# --------------------------
st.set_page_config(page_title="Text Analysis App", layout="wide")

tabs = st.tabs(["Text Summary", "Tab2", "Tab3", "Tab4", "Tab5"])

with tabs[0]:
    st.header("📝 Text Analysis: Summary and Tools")
    st.markdown("Provide your text below to get summary information and use analysis tools.")
    text_input = st.text_area("Enter your text here:", height=300)
    submit = st.button("🎯 Submit", key="submit_text")

    if submit and text_input.strip():
        # Summary
        words = re.findall(r'\b\w+\b', text_input)
        sentences = re.split(r'[.!?]+', text_input)
        passages = [p.strip() for p in re.split(r'\n+', text_input.strip()) if p.strip()]



        st.markdown("### 🔍 Text Summary")
        st.write(f"**Word Count:** {len(words)}")
        st.write(f"**Sentence Count:** {len([s for s in sentences if s.strip()])}")
        st.write(f"**Passage Count:** {len(passages)}")


        # Stop words input
        stopwords_input = st.text_input("(Optional) Enter words to exclude in the list (comma-separated):", "")

        col1, col2 = st.columns(2)

        # Button 1: Word Frequency
        with col1:
            if st.button("🟠 Make a Word List by Frequency", key="freq_btn"):
                stopwords = [w.strip().lower() for w in stopwords_input.split(",") if w.strip()]
                word_list = re.findall(r'\b\w+\b', text_input)
                filtered_words = []

                for word in word_list:
                    if word.lower() not in stopwords:
                        # Keep proper nouns with capitals
                        if word[0].isupper():
                            filtered_words.append(word)
                        else:
                            filtered_words.append(word.lower())

                freq_dist = Counter(filtered_words)
                df_freq = pd.DataFrame(freq_dist.items(), columns=["Word", "Frequency"]).sort_values(by="Frequency", ascending=False)
                st.dataframe(df_freq)

        # Button 2: Sentence View + CSV Download
        with col2:
            if st.button("🟠 Make a Sentence List", key="sent_btn"):
                sent_list = re.split(r'(?<=[.!?])\s+', text_input.strip())
                df_sent = pd.DataFrame({"Sentence": [s.strip() for s in sent_list if s.strip()]})
                st.dataframe(df_sent)

                csv = df_sent.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Download Sentences as CSV",
                    data=csv,
                    file_name='sentences.csv',
                    mime='text/csv'
                )

    else:
        st.info("Please enter your text to begin analysis.")

st.markdown("""
    <style>
        div.stButton > button:first-child {
            background-color: #FFD700 !important;  /* Yellow */
            color: black !important;
            font-weight: bold;
        }
        div.stButton > button:not(:first-child) {
            background-color: #1f77b4 !important;  /* Blue */
            color: white !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)
