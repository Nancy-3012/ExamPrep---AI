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

# ------------------ SESSION STATE ------------------
if "step" not in st.session_state:
    st.session_state.step = 1

# ------------------ STEP 1: USER INFO ------------------
if st.session_state.step == 1:

    st.title("👋 Welcome to ExamPrep AI")
    st.markdown("### Your Smart Study & Quiz Assistant")

    name = st.text_input("Enter your name")
    subject = st.text_input("Enter subject")

    if st.button("Continue ➡"):
        if name and subject:
            st.session_state.name = name
            st.session_state.subject = subject
            st.session_state.step = 2
        else:
            st.warning("Please fill all fields")

# ------------------ STEP 2: MODE SELECTION ------------------
elif st.session_state.step == 2:

    st.title(f"Welcome {st.session_state.name} 👋")
    st.markdown(f"### Subject: {st.session_state.subject}")

    st.markdown("---")
    st.subheader("Choose Mode")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📘 Preparation Mode"):
            st.session_state.mode = "prep"
            st.session_state.step = 3

    with col2:
        if st.button("🎯 Quiz Mode"):
            st.session_state.mode = "quiz"
            st.session_state.step = 3

    # 🔙 BACK BUTTON
    if st.button("🔙 Back"):
        st.session_state.step = 1

# ------------------ STEP 3: MAIN APP ------------------
elif st.session_state.step == 3:

    # 🔙 NAVIGATION BUTTONS
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔙 Change Mode"):
            st.session_state.step = 2

    with col2:
        if st.button("🔄 Restart"):
            reset_app()

    st.title("📘 ExamPrep AI")
    st.markdown(f"👤 User: **{st.session_state.name}**")
    st.markdown(f"📚 Subject: **{st.session_state.subject}**")
    st.markdown(f"⚙ Mode: **{st.session_state.mode.upper()}**")

    st.markdown("---")

    uploaded_file = st.file_uploader("📂 Upload PDF", type=["pdf"])
    num_questions = st.selectbox("📊 Number of Questions", [5, 10, 15])
    query = st.text_input("🔍 Enter topic")

    generate = st.button("🚀 Start")

    if uploaded_file is not None:

        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())

        # Step 1: Load + Clean
        raw_text = load_pdf("temp.pdf")
        cleaned_text = clean_text(raw_text)

        # Step 2: Chunking
        chunker = TextChunker()
        chunks = chunker.split_text(cleaned_text)

        st.success(f"📄 Document processed into {len(chunks)} chunks")

        if len(chunks) > 0:

            # Step 3: Embeddings
            embedder = Embedder()
            embeddings = embedder.embed_texts(chunks)

            # Step 4: Vector DB
            vector_db = VectorStore(len(embeddings[0]))
            vector_db.add_embeddings(embeddings, chunks)

            # Step 5: Retriever
            retriever = Retriever(vector_db, embedder)

            if generate and query:

                with st.spinner("Processing... ⏳"):

                    results = retriever.retrieve(query)
                    context = "\n".join(results)

                    generator = QuestionGenerator()
                    mcq, short_answer, viva = generator.generate_questions(context)

                    st.success("✅ Done!")

                    # ------------------ PREPARATION MODE ------------------
                    if st.session_state.mode == "prep":

                        with st.expander("📘 MCQ Questions", expanded=True):

                            for i, q in enumerate(mcq[:num_questions]):

                                st.markdown(f"### Q{i+1}. {q['question']}")

                                for j, opt in enumerate(q["options"]):
                                    st.markdown(f"{chr(65+j)}) {opt}")

                                st.markdown(f"**Answer:** {q['answer']}")
                                st.markdown("---")

                        with st.expander("✏ Short Answer Questions"):
                            for q in short_answer[:num_questions]:
                                st.write("- " + q)

                        with st.expander("🎤 Viva Questions"):
                            for q in viva[:num_questions]:
                                st.write("- " + q)

                    # ------------------ QUIZ MODE ------------------
                    else:

                        st.subheader("🎯 Quiz Time!")

                        score = 0

                        for i, q in enumerate(mcq[:num_questions]):

                            st.markdown(f"### Q{i+1}. {q['question']}")

                            user_ans = st.radio(
                                "Choose your answer:",
                                q["options"],
                                key=f"q{i}"
                            )

                            if st.button(f"Submit Q{i+1}", key=f"btn{i}"):

                                if user_ans == q["answer"]:
                                    st.success("✅ Correct!")
                                    score += 1
                                else:
                                    st.error(f"❌ Wrong! Correct: {q['answer']}")

                        st.markdown(f"### 🏆 Your Score: {score}/{num_questions}")

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("Made with ❤️ | ExamPrep AI")