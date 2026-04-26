import streamlit as st
from gtts import gTTS
import io

st.set_page_config(page_title="Easy English Word Quiz", layout="centered")

st.title("✨신나는 영어 단어 퀴즈🚌")
st.caption("그림을 보고, 발음을 들은 뒤 알맞은 영어 단어를 고르세요.")

TOTAL_QUESTIONS = 20

# ---------------------------
# 단어 듣기 함수
# ---------------------------
@st.cache_data
def make_audio(word):
    tts = gTTS(text=word, lang="en", tld="com", slow=False)
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    return audio_fp.getvalue()


# ---------------------------
# 단어 목록 20개
# answer: 정답 영어 단어
# meaning: 마지막 정답 확인용 한국어 뜻
# choices: 영어 보기 3지선다
# ---------------------------
word_data = [
    {"word": "run", "answer": "run", "meaning": "달리다", "picture": "🏃", "choices": ["run", "swim", "read"]},
    {"word": "talk", "answer": "talk", "meaning": "말하다", "picture": "🗣️", "choices": ["sit", "talk", "close"]},
    {"word": "eat", "answer": "eat", "meaning": "먹다", "picture": "🍽️", "choices": ["sleep", "walk", "eat"]},
    {"word": "sleep", "answer": "sleep", "meaning": "자다", "picture": "😴", "choices": ["laugh", "sleep", "drink"]},
    {"word": "drink", "answer": "drink", "meaning": "마시다", "picture": "🥤", "choices": ["open", "throw", "drink"]},

    {"word": "go", "answer": "go", "meaning": "가다", "picture": "➡️", "choices": ["go", "come", "see"]},
    {"word": "come", "answer": "come", "meaning": "오다", "picture": "👋", "choices": ["write", "listen", "come"]},
    {"word": "see", "answer": "see", "meaning": "보다", "picture": "👀", "choices": ["sell", "see", "wash"]},
    {"word": "read", "answer": "read", "meaning": "읽다", "picture": "📖", "choices": ["read", "cry", "make"]},
    {"word": "write", "answer": "write", "meaning": "쓰다", "picture": "✏️", "choices": ["ride", "close", "write"]},

    {"word": "open", "answer": "open", "meaning": "열다", "picture": "📂", "choices": ["wash", "open", "laugh"]},
    {"word": "close", "answer": "close", "meaning": "닫다", "picture": "🚪", "choices": ["close", "dance", "help"]},
    {"word": "sit", "answer": "sit", "meaning": "앉다", "picture": "🪑", "choices": ["stand", "cut", "sit"]},
    {"word": "stand", "answer": "stand", "meaning": "서다", "picture": "🧍", "choices": ["fly", "stand", "draw"]},
    {"word": "walk", "answer": "walk", "meaning": "걷다", "picture": "🚶", "choices": ["walk", "sing", "swim"]},

    {"word": "jump", "answer": "jump", "meaning": "뛰다", "picture": "🤾", "choices": ["wait", "learn", "jump"]},
    {"word": "laugh", "answer": "laugh", "meaning": "웃다", "picture": "😂", "choices": ["give", "laugh", "finish"]},
    {"word": "cry", "answer": "cry", "meaning": "울다", "picture": "😭", "choices": ["cry", "find", "lose"]},
    {"word": "sing", "answer": "sing", "meaning": "노래하다", "picture": "🎤", "choices": ["wake up", "study", "sing"]},
    {"word": "swim", "answer": "swim", "meaning": "수영하다", "picture": "🏊", "choices": ["cook", "swim", "clean"]},
]


# ---------------------------
# 세션 상태 초기화
# ---------------------------
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = word_data.copy()

if "stage" not in st.session_state:
    # 1: 1차 풀이
    # 1.5: 1차 응원 화면
    # 2: 2차 풀이
    # 2.5: 2차 응원 화면
    # 3: 최종 결과 및 정답 공개
    st.session_state.stage = 1

if "wrong_indices" not in st.session_state:
    st.session_state.wrong_indices = []

if "final_wrong_indices" not in st.session_state:
    st.session_state.final_wrong_indices = []

if "first_score" not in st.session_state:
    st.session_state.first_score = 0

if "second_score" not in st.session_state:
    st.session_state.second_score = 0

if "final_score" not in st.session_state:
    st.session_state.final_score = 0

if "first_celebration_shown" not in st.session_state:
    st.session_state.first_celebration_shown = False

if "second_celebration_shown" not in st.session_state:
    st.session_state.second_celebration_shown = False


# ---------------------------
# 다시 시작
# ---------------------------
if st.button("처음부터 다시 시작"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.markdown("---")

quiz_data = st.session_state.quiz_data


# ---------------------------
# 문제 화면 출력 함수
# ---------------------------
def show_question(i, item, radio_key, label):
    picture = item.get("picture", "❓")

    st.write(f"### {i+1}. Look, listen, and choose the English word.")
    st.caption("그림을 보고, 발음을 들은 뒤 알맞은 영어 단어를 고르세요.")

    # 이모지 그림
    st.markdown(
        f"""
        <div style="
            width: 120px;
            background-color: #f8fbff;
            border: 1.5px solid #dfe8ff;
            border-radius: 16px;
            padding: 10px;
            margin-top: 6px;
            margin-bottom: 10px;
            text-align: center;
            box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        ">
            <div style="
                font-size: 54px;
                line-height: 1.1;
            ">
                {picture}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 발음 듣기
    audio_bytes = make_audio(item["word"])
    st.audio(audio_bytes, format="audio/mp3")

    # 영어 단어 3지선다
    st.radio(
        label,
        item["choices"],
        key=radio_key,
        index=None
    )

    st.markdown("---")


# ---------------------------
# 1단계: 전체 문제 풀이
# ---------------------------
if st.session_state.stage == 1:
    st.subheader("1차 풀이")
    st.caption("그림과 발음을 확인한 뒤 알맞은 영어 단어를 고르세요.")

    for i, item in enumerate(quiz_data):
        show_question(i, item, f"q1_{i}", "영어 단어를 고르세요.")

    if st.button("1차 제출"):
        wrong_indices = []
        correct_count = 0

        for i, item in enumerate(quiz_data):
            user_answer = st.session_state.get(f"q1_{i}")

            if user_answer == item["answer"]:
                correct_count += 1
            else:
                wrong_indices.append(i)

        st.session_state.first_score = correct_count
        st.session_state.wrong_indices = wrong_indices
        st.session_state.first_celebration_shown = False
        st.session_state.stage = 1.5

        st.rerun()


# ---------------------------
# 1.5단계: 1차 응원 화면
# ---------------------------
elif st.session_state.stage == 1.5:
    score = st.session_state.first_score
    wrong_count = len(st.session_state.wrong_indices)

    if not st.session_state.first_celebration_shown:
        st.balloons()
        st.session_state.first_celebration_shown = True

    st.subheader("🎉 1차 풀이 완료!")

    st.success("잘했어요! 그림과 발음을 연결해서 영어 단어를 고르는 연습을 잘 해냈습니다.")

    st.write(f"1차에서 **{score}문제**를 맞혔습니다.")
    st.write(f"다시 풀 단어는 **{wrong_count}개**입니다.")

    st.info("틀린 단어는 아직 익숙하지 않은 단어일 뿐입니다. 다시 들으면 더 잘 기억할 수 있어요!")

    st.progress(score / TOTAL_QUESTIONS)

    if score == TOTAL_QUESTIONS:
        st.success("완벽합니다! 1차에서 모든 단어를 맞혔습니다.")
        if st.button("최종 결과 보기"):
            st.session_state.final_score = TOTAL_QUESTIONS
            st.session_state.second_score = 0
            st.session_state.final_wrong_indices = []
            st.session_state.stage = 3
            st.rerun()
    else:
        if st.button("2차 오답 다시 풀기 시작하기"):
            st.session_state.stage = 2
            st.rerun()


# ---------------------------
# 2단계: 오답 문제 다시 풀이
# ---------------------------
elif st.session_state.stage == 2:
    wrong_indices = st.session_state.wrong_indices

    st.subheader("2차 풀이")
    st.write(f"1차 점수: **{st.session_state.first_score} / {TOTAL_QUESTIONS}**")
    st.warning(f"다시 풀 단어: {len(wrong_indices)}개")

    st.markdown("---")
    st.caption("1차에서 틀린 단어만 다시 풉니다. 그림을 보고 발음을 다시 들어 보세요.")

    for idx in wrong_indices:
        item = quiz_data[idx]
        show_question(idx, item, f"q2_{idx}", "다시 영어 단어를 고르세요.")

    if st.button("2차 제출"):
        additional_correct = 0
        final_wrong_indices = []

        for idx in wrong_indices:
            item = quiz_data[idx]
            retry_answer = st.session_state.get(f"q2_{idx}")

            if retry_answer == item["answer"]:
                additional_correct += 1
            else:
                final_wrong_indices.append(idx)

        st.session_state.second_score = additional_correct
        st.session_state.final_score = st.session_state.first_score + additional_correct
        st.session_state.final_wrong_indices = final_wrong_indices
        st.session_state.second_celebration_shown = False
        st.session_state.stage = 2.5

        st.rerun()


# ---------------------------
# 2.5단계: 2차 응원 화면
# ---------------------------
elif st.session_state.stage == 2.5:
    retry_total = len(st.session_state.wrong_indices)
    second_score = st.session_state.second_score
    final_score = st.session_state.final_score
    final_wrong_count = len(st.session_state.final_wrong_indices)

    if not st.session_state.second_celebration_shown:
        st.balloons()
        st.session_state.second_celebration_shown = True

    st.subheader("🌟 2차 풀이 완료!")

    st.success("끝까지 다시 도전한 것이 정말 멋집니다!")

    st.write(f"2차에서 **{retry_total}개 중 {second_score}개**를 다시 맞혔습니다.")
    st.write(f"현재 최종 점수는 **{final_score} / {TOTAL_QUESTIONS}**입니다.")

    st.info("한 번 틀린 단어를 다시 맞혔다는 것은, 소리와 철자가 더 잘 연결되고 있다는 뜻입니다.")

    st.progress(final_score / TOTAL_QUESTIONS)

    if final_wrong_count == 0:
        st.success("대단합니다! 2차까지 모두 해결했습니다.")
    else:
        st.info(f"아직 헷갈린 단어는 {final_wrong_count}개입니다. 마지막 정답 확인에서 다시 정리해 봅시다.")

    if st.button("최종 결과와 정답 확인하기"):
        st.session_state.stage = 3
        st.rerun()


# ---------------------------
# 3단계: 최종 결과 + 정답 공개
# ---------------------------
elif st.session_state.stage == 3:
    st.subheader("최종 결과")

    st.write(f"1차 점수: **{st.session_state.first_score} / {TOTAL_QUESTIONS}**")
    st.write(f"2차에서 다시 맞힌 단어 수: **{st.session_state.second_score}개**")
    st.write(f"최종 점수: **{st.session_state.final_score} / {TOTAL_QUESTIONS}**")

    if st.session_state.final_score == TOTAL_QUESTIONS:
        st.success("만점입니다! 정말 훌륭합니다! 🎉")
        st.balloons()
    elif st.session_state.final_score >= 16:
        st.success("아주 잘했습니다! 단어의 소리와 철자를 잘 연결하고 있어요!")
    elif st.session_state.final_score >= 12:
        st.info("잘했습니다. 조금만 더 연습하면 더 많은 단어를 정확히 들을 수 있습니다.")
    else:
        st.warning("괜찮습니다. 헷갈린 단어를 다시 보면서 천천히 익혀 봅시다.")

    st.markdown("---")
    st.subheader("정답 확인")

    final_wrong_indices = st.session_state.get("final_wrong_indices", [])

    for i, item in enumerate(quiz_data):
        picture = item.get("picture", "❓")
        word_display = item["word"]

        st.write(f"### {i+1}. {word_display}")

        st.markdown(
            f"""
            <div style="
                width: 110px;
                background-color: #fffdf7;
                border: 1.5px solid #ffe7b8;
                border-radius: 16px;
                padding: 10px;
                margin-top: 6px;
                margin-bottom: 10px;
                text-align: center;
                box-shadow: 0 2px 6px rgba(0,0,0,0.04);
            ">
                <div style="
                    font-size: 50px;
                    line-height: 1.1;
                ">
                    {picture}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        audio_bytes = make_audio(item["word"])
        st.audio(audio_bytes, format="audio/mp3")

        first_answer = st.session_state.get(f"q1_{i}")
        second_answer = st.session_state.get(f"q2_{i}") if f"q2_{i}" in st.session_state else None

        st.write(f"- 정답 영어 단어: **{item['answer']}**")
        st.write(f"- 뜻: **{item['meaning']}**")

        if second_answer is not None:
            st.write(f"- 1차 선택: {first_answer if first_answer else '미응답'}")
            st.write(f"- 2차 선택: {second_answer if second_answer else '미응답'}")

            if i in final_wrong_indices:
                st.error("최종 오답")
            else:
                st.success("2차에서 정답")
        else:
            st.write(f"- 선택: {first_answer if first_answer else '미응답'}")

            if first_answer == item["answer"]:
                st.success("1차에서 정답")
            else:
                st.error("오답")

        st.markdown("---")
