import streamlit as st

st.set_page_config(page_title="Tense Practice", layout="centered")

st.title("⏳ Tense Practice")
st.caption("한 문제씩 풀고, 맞으면 풍선이 터집니다. 틀린 문제는 2차에서 다시 풉니다.")

TOTAL_QUESTIONS = 20

# ---------------------------
# 문제 목록
# ---------------------------
quiz_data = [
    {
        "sentence": "She (     ) a book now.",
        "answer": "is reading",
        "choices": ["reads", "is reading", "read", "will read"]
    },
    {
        "sentence": "They (     ) soccer yesterday.",
        "answer": "played",
        "choices": ["play", "are playing", "played", "will play"]
    },
    {
        "sentence": "I (     ) breakfast every morning.",
        "answer": "eat",
        "choices": ["am eating", "ate", "will eat", "eat"]
    },
    {
        "sentence": "He (     ) his friend tomorrow.",
        "answer": "will meet",
        "choices": ["meets", "met", "will meet", "is meeting"]
    },
    {
        "sentence": "We (     ) English now.",
        "answer": "are studying",
        "choices": ["studied", "study", "are studying", "will study"]
    },
    {
        "sentence": "My father (     ) coffee every day.",
        "answer": "drinks",
        "choices": ["drinks", "is drinking", "drank", "will drink"]
    },
    {
        "sentence": "The students (     ) to the teacher now.",
        "answer": "are listening",
        "choices": ["listen", "listened", "will listen", "are listening"]
    },
    {
        "sentence": "I (     ) my homework last night.",
        "answer": "did",
        "choices": ["do", "am doing", "did", "will do"]
    },
    {
        "sentence": "She (     ) to school by bus every day.",
        "answer": "goes",
        "choices": ["is going", "went", "will go", "goes"]
    },
    {
        "sentence": "He (     ) TV now.",
        "answer": "is watching",
        "choices": ["watched", "watches", "is watching", "will watch"]
    },
    {
        "sentence": "We (     ) a movie tomorrow.",
        "answer": "will watch",
        "choices": ["watch", "watched", "are watching", "will watch"]
    },
    {
        "sentence": "They (     ) in the park last Sunday.",
        "answer": "walked",
        "choices": ["walked", "walk", "are walking", "will walk"]
    },
    {
        "sentence": "My brother (     ) computer games every weekend.",
        "answer": "plays",
        "choices": ["is playing", "played", "plays", "will play"]
    },
    {
        "sentence": "Look! The baby (     ).",
        "answer": "is sleeping",
        "choices": ["sleeps", "slept", "will sleep", "is sleeping"]
    },
    {
        "sentence": "I (     ) my grandmother next week.",
        "answer": "will visit",
        "choices": ["visit", "visited", "am visiting", "will visit"]
    },
    {
        "sentence": "She (     ) a letter yesterday.",
        "answer": "wrote",
        "choices": ["writes", "is writing", "wrote", "will write"]
    },
    {
        "sentence": "Tom (     ) up at seven every morning.",
        "answer": "gets",
        "choices": ["got", "gets", "is getting", "will get"]
    },
    {
        "sentence": "We (     ) lunch now.",
        "answer": "are having",
        "choices": ["have", "had", "are having", "will have"]
    },
    {
        "sentence": "It (     ) tomorrow.",
        "answer": "will rain",
        "choices": ["rains", "rained", "is raining", "will rain"]
    },
    {
        "sentence": "He (     ) a new bike last month.",
        "answer": "bought",
        "choices": ["buys", "is buying", "bought", "will buy"]
    },
]

# ---------------------------
# 세션 상태 초기화
# ---------------------------
if "stage" not in st.session_state:
    # round1: 1차 풀이
    # round2: 오답 다시 풀기
    # final: 최종 결과
    st.session_state.stage = "round1"

if "q_index" not in st.session_state:
    st.session_state.q_index = 0

if "checked" not in st.session_state:
    st.session_state.checked = False

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

if "first_score" not in st.session_state:
    st.session_state.first_score = 0

if "second_score" not in st.session_state:
    st.session_state.second_score = 0

if "wrong_indices" not in st.session_state:
    st.session_state.wrong_indices = []

if "final_wrong_indices" not in st.session_state:
    st.session_state.final_wrong_indices = []

if "first_answers" not in st.session_state:
    st.session_state.first_answers = {}

if "second_answers" not in st.session_state:
    st.session_state.second_answers = {}

# ---------------------------
# 처음부터 다시 시작
# ---------------------------
if st.button("처음부터 다시 시작"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.markdown("---")

# ---------------------------
# 정답 확인 함수
# ---------------------------
def check_answer(item, user_answer):
    return user_answer == item["answer"]

# ---------------------------
# 다음 문제로 이동
# ---------------------------
def go_next_round1():
    st.session_state.q_index += 1
    st.session_state.checked = False
    st.session_state.feedback = ""

    if st.session_state.q_index >= TOTAL_QUESTIONS:
        if len(st.session_state.wrong_indices) > 0:
            st.session_state.stage = "round2"
            st.session_state.q_index = 0
        else:
            st.session_state.stage = "final"

def go_next_round2():
    st.session_state.q_index += 1
    st.session_state.checked = False
    st.session_state.feedback = ""

    if st.session_state.q_index >= len(st.session_state.wrong_indices):
        st.session_state.stage = "final"

# ---------------------------
# 1차 풀이
# ---------------------------
if st.session_state.stage == "round1":
    st.subheader("1차 풀이")

    progress_text = f"{st.session_state.q_index + 1} / {TOTAL_QUESTIONS}"
    st.progress((st.session_state.q_index + 1) / TOTAL_QUESTIONS)
    st.caption(f"진행 상황: {progress_text}")

    i = st.session_state.q_index
    item = quiz_data[i]

    st.write(f"### {i+1}. {item['sentence']}")

    user_answer = st.radio(
        "정답을 고르세요.",
        item["choices"],
        key=f"q1_{i}",
        index=None
    )

    if not st.session_state.checked:
        if st.button("정답 확인"):
            if user_answer is None:
                st.warning("먼저 답을 고르세요.")
            else:
                st.session_state.first_answers[i] = user_answer

                if check_answer(item, user_answer):
                    st.session_state.first_score += 1
                    st.session_state.feedback = "correct"
                    st.session_state.checked = True
                    st.balloons()
                else:
                    if i not in st.session_state.wrong_indices:
                        st.session_state.wrong_indices.append(i)
                    st.session_state.feedback = "wrong"
                    st.session_state.checked = True

                st.rerun()

    else:
        if st.session_state.feedback == "correct":
            st.success("정답입니다! 🎉")
        elif st.session_state.feedback == "wrong":
            st.error("오답입니다. 이 문제는 2차에서 다시 나옵니다.")

        if st.button("다음 문제"):
            go_next_round1()
            st.rerun()

# ---------------------------
# 2차 풀이: 1차 오답만 다시 풀기
# ---------------------------
elif st.session_state.stage == "round2":
    st.subheader("2차 풀이")
    st.caption("1차에서 틀린 문제만 다시 풉니다.")

    total_wrong = len(st.session_state.wrong_indices)
    current_retry_number = st.session_state.q_index + 1

    st.progress(current_retry_number / total_wrong)
    st.caption(f"오답 다시 풀기: {current_retry_number} / {total_wrong}")

    original_idx = st.session_state.wrong_indices[st.session_state.q_index]
    item = quiz_data[original_idx]

    st.write(f"### {original_idx + 1}. {item['sentence']}")

    user_answer = st.radio(
        "다시 정답을 고르세요.",
        item["choices"],
        key=f"q2_{original_idx}",
        index=None
    )

    if not st.session_state.checked:
        if st.button("정답 확인"):
            if user_answer is None:
                st.warning("먼저 답을 고르세요.")
            else:
                st.session_state.second_answers[original_idx] = user_answer

                if check_answer(item, user_answer):
                    st.session_state.second_score += 1
                    st.session_state.feedback = "correct"
                    st.session_state.checked = True
                    st.balloons()
                else:
                    if original_idx not in st.session_state.final_wrong_indices:
                        st.session_state.final_wrong_indices.append(original_idx)
                    st.session_state.feedback = "wrong"
                    st.session_state.checked = True

                st.rerun()

    else:
        if st.session_state.feedback == "correct":
            st.success("2차에서 정답입니다! 🎉")
        elif st.session_state.feedback == "wrong":
            st.error("아쉽습니다. 최종 오답으로 기록됩니다.")

        if st.button("다음 문제"):
            go_next_round2()
            st.rerun()

# ---------------------------
# 최종 결과
# ---------------------------
elif st.session_state.stage == "final":
    final_score = st.session_state.first_score + st.session_state.second_score

    st.subheader("최종 결과")

    st.write(f"1차 점수: **{st.session_state.first_score} / {TOTAL_QUESTIONS}**")
    st.write(f"2차에서 맞힌 문제 수: **{st.session_state.second_score} / {len(st.session_state.wrong_indices)}**")
    st.write(f"최종 점수: **{final_score} / {TOTAL_QUESTIONS}**")

    if final_score == TOTAL_QUESTIONS:
        st.success("만점입니다! 아주 잘했습니다! 🎉")
        st.balloons()
    elif final_score >= 16:
        st.success("아주 잘했습니다!")
    elif final_score >= 12:
        st.info("잘했습니다.")
    else:
        st.warning("조금 더 연습해 봅시다.")

    st.markdown("---")
    st.subheader("정답 및 오답 확인")

    if len(st.session_state.final_wrong_indices) == 0:
        st.success("최종 오답이 없습니다.")
    else:
        st.error(f"최종 오답: {len(st.session_state.final_wrong_indices)}문제")

    for i, item in enumerate(quiz_data):
        first_answer = st.session_state.first_answers.get(i, "미응답")
        second_answer = st.session_state.second_answers.get(i, None)

        st.write(f"### {i+1}. {item['sentence']}")
        st.write(f"- 정답: **{item['answer']}**")
        st.write(f"- 1차 선택: {first_answer}")

        if i in st.session_state.wrong_indices:
            st.write(f"- 2차 선택: {second_answer if second_answer else '미응답'}")

            if i in st.session_state.final_wrong_indices:
                st.error("최종 오답")
            else:
                st.success("2차에서 정답")
        else:
            st.success("1차에서 정답")

        st.markdown("---")
