import streamlit as st

from src.data_processing.pdf_loader import load_pdf
from src.data_processing.cleaner import clean_text
from src.chunking.chunker import TextChunker
from src.embeddings.embedder import Embedder
from src.embeddings.vector_store import VectorStore
from src.rag.retriever import Retriever
from src.rag.question_generator import QuestionGenerator

st.set_page_config(page_title="ExamPrep AI", layout="centered")

# ------------------ RESET FUNCTION ------------------
def reset_app():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# ------------------ SESSION ------------------
if "step" not in st.session_state:
    st.session_state.step = 1

# ------------------ STEP 1 ------------------
if st.session_state.step == 1:

    st.title("👋 Welcome to ExamPrep AI")

    name = st.text_input("Enter your name")
    subject = st.text_input("Enter subject")

    if st.button("Continue ➡"):
        if name and subject:
            st.session_state.name = name
            st.session_state.subject = subject
            st.session_state.step = 2

# ------------------ STEP 2 ------------------
elif st.session_state.step == 2:

    st.title(f"Welcome {st.session_state.name}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📘 Preparation Mode"):
            st.session_state.mode = "prep"
            st.session_state.step = 3

    with col2:
        if st.button("🎯 Quiz Mode"):
            st.session_state.mode = "quiz"
            st.session_state.step = 3

    if st.button("🔙 Back"):
        st.session_state.step = 1

# ------------------ STEP 3 ------------------
elif st.session_state.step == 3:

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔙 Change Mode"):
            st.session_state.step = 2

    with col2:
        if st.button("🔄 Restart"):
            reset_app()

    st.title("📘 ExamPrep AI")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    num_questions = st.selectbox("Number of Questions", [5, 10, 15])
    query = st.text_input("Enter topic")

    # -------- GENERATE --------
    if st.button("Start"):

        if uploaded_file and query:

            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.read())

            raw_text = load_pdf("temp.pdf")
            cleaned_text = clean_text(raw_text)

            chunker = TextChunker()
            chunks = chunker.split_text(cleaned_text)

            embedder = Embedder()
            embeddings = embedder.embed_texts(chunks)

            vector_db = VectorStore(len(embeddings[0]))
            vector_db.add_embeddings(embeddings, chunks)

            retriever = Retriever(vector_db, embedder)
            results = retriever.retrieve(query)

            context = "\n".join(results)

            generator = QuestionGenerator()
            mcq, short_answer, viva = generator.generate_questions(context)

            st.session_state.mcq = mcq[:num_questions]
            st.session_state.generated = True
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.answers = {}

    # -------- AFTER GENERATION --------
    if st.session_state.get("generated"):

        # ------------------ PREP MODE ------------------
        if st.session_state.mode == "prep":

            for i, q in enumerate(st.session_state.mcq):
                st.markdown(f"### Q{i+1}. {q['question']}")
                for opt in q["options"]:
                    st.write(opt)
                st.success(f"Answer: {q['answer']}")
                st.markdown("---")

        # ------------------ QUIZ MODE ------------------
        else:

            q_index = st.session_state.current_q
            total = len(st.session_state.mcq)

            # -------- QUIZ FINISHED --------
            if q_index >= total:

                st.success("🎉 Quiz Completed!")
                st.markdown(f"## 🏆 Score: {st.session_state.score}/{total}")

                st.markdown("## 📊 Review Answers")

                for i, q in enumerate(st.session_state.mcq):

                    user_ans = st.session_state.answers.get(i)
                    correct_ans = q["answer"]

                    st.markdown(f"### Q{i+1}. {q['question']}")

                    st.write(f"Your Answer: {user_ans}")

                    if user_ans == correct_ans:
                        st.success("✅ Correct")
                    else:
                        st.error(f"❌ Wrong | Correct: {correct_ans}")

                    st.markdown("---")

                st.stop()

            # -------- CURRENT QUESTION --------
            question = st.session_state.mcq[q_index]

            st.markdown(f"### Question {q_index+1} / {total}")

            # NO DEFAULT SELECTION
            selected = st.radio(
                question["question"],
                ["-- Select an option --"] + question["options"],
                index=0,
                key=f"q_{q_index}"
            )

            # -------- NEXT BUTTON --------
            if st.button("Next ➡"):

                if selected == "-- Select an option --":
                    st.warning("⚠ Please select an option")
                else:

                    st.session_state.answers[q_index] = selected

                    if selected == question["answer"]:
                        st.session_state.score += 1

                    st.session_state.current_q += 1
                    st.rerun()

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("Made with ❤️ | ExamPrep AI")