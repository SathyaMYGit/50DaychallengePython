import streamlit as st

st.title("🧠 Simple Quiz App")

# Questions and answers
questions = {
    "What is the capital of France?": "Paris",
    "Which planet is known as the Red Planet?": "Mars",
    "What is 5 + 3?": "8",
    "Who wrote 'Hamlet'?": "Shakespeare"
}

score = 0

# Ask questions
for q, a in questions.items():
    user_answer = st.text_input(f"{q}")
    if user_answer:
        if user_answer.strip().lower() == a.lower():
            st.success("✅ Correct!")
            score += 1
        else:
            st.error(f"❌ Wrong! Correct answer is: {a}")

# Show final score
if st.button("Show Score"):
    st.info(f"Your score is: {score} out of {len(questions)}")
