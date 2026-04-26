import streamlit as st
import random

st.set_page_config(page_title="영어 시제 퀴즈", layout="centered")

st.title("⏳ Alex선생님과 함께하는 영어 시제 퀴즈")
st.caption("빈칸에 알맞은 표현을 고르는 30문제 · 4지선다 퀴즈")

# ---------------------------
# 문제 데이터
# ---------------------------
question_data = [
    {
        "question": "She (     ) a book now.",
        "answer": "is reading",
        "choices": ["is reading", "reads", "read", "will read"]
    },
    {
        "question": "I (     ) lunch every day.",
        "answer": "eat",
        "choices": ["am eating", "eat", "ate", "will eat"]
    },
    {
        "question": "They (     ) soccer yesterday.",
        "answer": "played",
        "choices": ["play", "are playing", "played", "will play"]
    },
    {
        "question": "He (     ) to school tomorrow.",
        "answer": "will go",
        "choices": ["goes", "went", "is going", "will go"]
    },
    {
        "question": "We (     ) TV now.",
        "answer": "are watching",
        "choices": ["watch", "watched", "are watching", "will watch"]
    },
    {
        "question": "My father (     ) coffee every morning.",
        "answer": "drinks",
        "choices": ["is drinking", "drinks", "drank", "will drink"]
    },
    {
        "question": "The baby (     ) last night.",
        "answer": "cried",
        "choices": ["cries", "is crying", "cried", "will cry"]
    },
    {
        "question": "I (     ) my homework tonight.",
        "answer": "will do",
        "choices": ["do", "am doing", "did", "will do"]
    },
    {
        "question": "She (     ) dinner now.",
        "answer": "is cooking",
        "choices": ["cooks", "cooked", "is cooking", "will cook"]
    },
    {
        "question": "He (     ) English very well.",
        "answer": "speaks",
        "choices": ["is speaking", "speaks", "spoke", "will speak"]
    },
    {
        "question": "We (     ) in the park yesterday.",
        "answer": "walked",
        "choices": ["walk", "are walking", "walked", "will walk"]
    },
    {
        "question": "They (     ) their grandma next weekend.",
        "answer": "will visit",
        "choices": ["visit", "visited", "are visiting", "will visit"]
    },
    {
        "question": "I (     ) to music now.",
        "answer": "am listening",
        "choices": ["listen", "listened", "am listening", "will listen"]
    },
    {
        "question": "She (     ) breakfast at 7 every day.",
        "answer": "has",
        "choices": ["is having", "has", "had", "will have"]
    },
    {
        "question": "My friends (     ) a movie last Saturday.",
        "answer": "watched",
        "choices": ["watch", "are watching", "watched", "will watch"]
    },
    {
        "question": "He (     ) his uncle next month.",
        "answer": "will meet",
        "choices": ["meets", "met", "is meeting", "will meet"]
    },
    {
        "question": "The students (     ) in the classroom now.",
        "answer": "are studying",
        "choices": ["study", "studied", "are studying", "will study"]
    },
    {
        "question": "My mother (     ) dinner every evening.",
        "answer": "makes",
        "choices": ["is making", "makes", "made", "will make"]
    },
    {
        "question": "I (     ) my phone at home yesterday.",
        "answer": "left",
        "choices": ["leave", "am leaving", "left", "will leave"]
    },
    {
        "question": "We (     ) to Busan next week.",
        "answer": "will travel",
        "choices": ["travel", "traveled", "are traveling", "will travel"]
    },
    {
        "question": "He (     ) a shower now.",
        "answer": "is taking",
        "choices": ["takes", "took", "is taking", "will take"]
    },
    {
        "question": "She (     ) the piano very well.",
        "answer": "plays",
        "choices": ["is playing", "plays", "played", "will play"]
    },
    {
        "question": "They (     ) late for school yesterday.",
        "answer": "were",
        "choices": ["are", "were", "will be", "being"]
    },
    {
        "question": "I (     ) busy tomorrow.",
        "answer": "will be",
        "choices": ["am", "was", "will be", "being"]
    },
    {
        "question": "The dog (     ) on the sofa now.",
        "answer": "is sleeping",
        "choices": ["sleeps", "slept", "is sleeping", "will sleep"]
    },
    {
        "question": "My brother (     ) basketball after school.",
        "answer": "plays",
        "choices": ["is playing", "plays", "played", "will play"]
    },
    {
        "question": "We (     ) our room yesterday.",
        "answer": "cleaned",
        "choices": ["clean", "are cleaning", "cleaned", "will clean"]
    },
    {
        "question": "She (     ) her friend this evening.",
        "answer": "will call",
        "choices": ["calls", "called", "is calling", "will call"]
    },
    {
        "question": "I (     ) a letter now.",
        "answer": "am writing",
        "choices": ["write", "wrote", "am writing", "will write"]
    },
    {
        "question": "He (     ) to bed at 10 every night.",
        "answer": "goes",
        "choices": ["is going", "goes", "went", "will go"]
    },
]

# ---------------------------
# 세션 상태 초기화
# ---------------------------
if "quiz_data" not in st.session_state:
    quiz_data = question_data.copy()
    random.shuffle(quiz_data)
    st.session_state.quiz_data = quiz_data

if "stage" not in st.session_state:
    # stage 1: 전체 풀이
    # stage 2: 오답 다시 풀이
    # stage 3: 최종 결과 및 정답 공개
    st.session_state.stage = 1

if "wrong_indices" not in st.session_state:
    st.session_state.wrong_indices = []

if "first_score" not in st.session_state:
    st.session_state.first_score = 0

if "final_score" not in st.session_state:
    st.session_state.final_score = 0

# ---------------------------
# 다시 시작 버튼
# ---------------------------
if st.button("처음부터 다시 시작"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.markdown("---")
quiz_data = st.session_state.quiz_data

# ---------------------------
# 1단계: 전체 문제 풀이
# ---------------------------
if st.session_state.stage == 1:
    st.subheader("1차 풀이")

    for i, item in enumerate(quiz_data):
        st.write(f"### {i+1}. {item['question']}")
        st.radio(
            "알맞은 답을 고르세요.",
            item["choices"],
            key=f"q1_{i}",
            index=None
        )

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

        if len(wrong_indices) == 0:
            st.session_state.final_score = 30
            st.session_state.stage = 3
        else:
            st.session_state.stage = 2

        st.rerun()

# ---------------------------
# 2단계: 오답 다시 풀기
# ---------------------------
elif st.session_state.stage == 2:
    first_score = st.session_state.first_score
    wrong_indices = st.session_state.wrong_indices

    st.subheader("1차 결과")
    st.write(f"점수: **{first_score} / 30**")
    st.warning(f"틀린 문제 수: {len(wrong_indices)}문제")

    st.markdown("---")
    st.subheader("오답 다시 풀기")
    st.caption("틀린 문제만 다시 풀고 제출하세요. 이후 정답이 공개됩니다.")

    for idx in wrong_indices:
        item = quiz_data[idx]
        st.write(f"### {idx+1}. {item['question']}")
        st.radio(
            "다시 정답을 고르세요.",
            item["choices"],
            key=f"q2_{idx}",
            index=None
        )

    if st.button("다시 풀기 제출"):
        additional_correct = 0

        for idx in wrong_indices:
            item = quiz_data[idx]
            retry_answer = st.session_state.get(f"q2_{idx}")
            if retry_answer == item["answer"]:
                additional_correct += 1

        st.session_state.final_score = st.session_state.first_score + additional_correct
        st.session_state.stage = 3
        st.rerun()

# ---------------------------
# 3단계: 최종 결과 + 정답 공개
# ---------------------------
elif st.session_state.stage == 3:
    st.subheader("최종 결과")
    st.write(f"1차 점수: **{st.session_state.first_score} / 30**")
    st.write(f"최종 점수: **{st.session_state.final_score} / 30**")

    if st.session_state.final_score == 30:
        st.success("만점입니다!")
        st.balloons()
    elif st.session_state.final_score >= 24:
        st.success("아주 잘했습니다!")
    elif st.session_state.final_score >= 18:
        st.info("잘했습니다.")
    else:
        st.warning("조금 더 연습해 봅시다.")

    st.markdown("---")
    st.subheader("정답 확인")

    for i, item in enumerate(quiz_data):
        first_answer = st.session_state.get(f"q1_{i}")
        second_answer = st.session_state.get(f"q2_{i}") if f"q2_{i}" in st.session_state else None

        st.write(f"### {i+1}. {item['question']}")
        st.write(f"- 정답: **{item['answer']}**")

        if second_answer is not None:
            st.write(f"- 1차 선택: {first_answer if first_answer else '미응답'}")
            st.write(f"- 2차 선택: {second_answer if second_answer else '미응답'}")
        else:
            st.write(f"- 선택: {first_answer if first_answer else '미응답'}")

        if second_answer is not None:
            if second_answer == item["answer"]:
                st.success("최종 정답")
            else:
                st.error("최종 오답")
        else:
            if first_answer == item["answer"]:
                st.success("정답")
            else:
                st.error("오답")
