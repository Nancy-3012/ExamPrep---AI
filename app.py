import streamlit as st

from src.data_processing.pdf_loader import load_pdf
from src.data_processing.cleaner import clean_text
from src.chunking.chunker import TextChunker
from src.embeddings.embedder import Embedder
from src.embeddings.vector_store import VectorStore
from src.rag.retriever import Retriever
from src.rag.question_generator import QuestionGenerator

st.set_page_config(page_title="ExamPrep AI", layout="centered")

st.title("📘 ExamPrep AI")
st.write("Upload your syllabus or notes and generate exam questions.")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

num_questions = st.selectbox("Number of questions", [5, 10, 15])

generate = st.button("Generate Questions")

if uploaded_file is not None:

    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    # Step 1: Load + Clean
    raw_text = load_pdf("temp.pdf")
    cleaned_text = clean_text(raw_text)

    # Step 2: Chunking
    chunker = TextChunker()
    chunks = chunker.split_text(cleaned_text)

    st.success(f"Document split into {len(chunks)} chunks")

    if len(chunks) > 0:

        # Step 3: Embeddings
        embedder = Embedder()
        embeddings = embedder.embed_texts(chunks)

        # Step 4: Vector DB
        vector_db = VectorStore(len(embeddings[0]))
        vector_db.add_embeddings(embeddings, chunks)

        # Step 5: Retriever
        retriever = Retriever(vector_db, embedder)

        # Step 6: Topic input
        query = st.text_input("Enter topic (e.g., cloud computing)")

        if generate and query:

            results = retriever.retrieve(query)
            context = "\n".join(results)

            # Step 7: Question Generation
            generator = QuestionGenerator()
            mcq, short_answer, viva = generator.generate_questions(context)

            st.subheader("📘 MCQ Questions")

            for q in mcq[:num_questions]:
                st.write(q["question"])

                for i, opt in enumerate(q["options"]):
                    st.write(f"{chr(65+i)}) {opt}")

                st.write(f"**Answer:** {q['answer']}")
                st.write("---")

            st.subheader("✏ Short Answer Questions")

            for q in short_answer[:num_questions]:
                st.write("- " + q)

            st.subheader("🎤 Viva Questions")

            for q in viva[:num_questions]:
                st.write("- " + q)