# Streamlit

+ Web link: https://streamlit.io


### 1. Overview
![streamlit](https://github.com/MK316/Applied-linguistics/raw/main/pages/images/streamlit-intro.png)


### 2. App deployment online

![streamlit](https://github.com/MK316/Applied-linguistics/raw/main/pages/images/deploy1.png)

### Sample app code: my TTS app

1. app.py code
   
```
import streamlit as st
from gtts import gTTS
import io

st.subheader("Text-to-Speech Converter (using Google TTS)")

text_input = st.text_area("Enter the text you want to convert to speech:")

language = st.selectbox(
    "Choose a language: 🇰🇷 🇺🇸 🇬🇧 🇷🇺 🇫🇷 🇪🇸 🇯🇵 ",
    [
        "Korean",
        "English (American)",
        "English (British)",
        "Russian",
        "Spanish",
        "French",
        "Japanese"
    ]
)

tts_button = st.button("Convert Text to Speech")

if tts_button and text_input:
    lang_codes = {
        "Korean": ("ko", None),
        "English (American)": ("en", "com"),
        "English (British)": ("en", "co.uk"),
        "Russian": ("ru", None),
        "Spanish": ("es", None),
        "French": ("fr", None),
        "Japanese": ("ja", None)
    }

    language_code, tld = lang_codes[language]

    if tld:
        tts = gTTS(text=text_input, lang=language_code, tld=tld, slow=False)
    else:
        tts = gTTS(text=text_input, lang=language_code, slow=False)

    speech = io.BytesIO()
    tts.write_to_fp(speech)
    speech.seek(0)

    st.audio(speech.getvalue(), format="audio/mp3")

st.markdown("---")
st.caption("🇺🇸 English text: Teacher-designed coding applications create tailored learning experiences, making complex concepts easier to understand through interactive and adaptive tools. They enhance engagement, provide immediate feedback, and support active learning.")
st.caption("🇰🇷 Korean text: 교사가 직접 만든 코딩 기반 애플리케이션은 학습자의 필요에 맞춘 학습 경험을 제공하고, 복잡한 개념을 쉽게 이해하도록 돕습니다. 또한 학습 몰입도를 높이고 즉각적인 피드백을 제공하며, 능동적인 학습을 지원합니다.")
st.caption("🇫🇷 French: Les applications de codage conçues par les enseignants offrent une expérience d'apprentissage personnalisée, rendant les concepts complexes plus faciles à comprendre grâce à des outils interactifs et adaptatifs. Elles améliorent l'engagement, fournissent un retour immédiat et soutiennent l'apprentissage actif.")
st.caption("🇷🇺 Russian: Созданные учителями кодированные приложения предлагают персонализированный опыт обучения, упрощая понимание сложных концепций с помощью интерактивных и адаптивных инструментов. Они повышают вовлеченность, предоставляют мгновенную обратную связь и поддерживают активное обучение.")
st.caption("🇨🇳 Chinese: 由教师设计的编程应用程序为学习者提供个性化的学习体验，通过互动和适应性工具使复杂的概念更容易理解。它们增强学习参与度，提供即时反馈，并支持主动学习。")
st.caption("🇯🇵 Japanese: 教師が設計したコーディングアプリケーションは、学習者のニーズに合わせた学習体験を提供し、複雑な概念をインタラクティブで適応性のあるツールを通じて理解しやすくします。また、学習への集中力を高め、即時フィードバックを提供し、主体的な学習をサポートします。")

```

2. requirements.txt

```
streamlit
gTTS
```
