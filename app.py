import streamlit as st
import json
import os
import sys
import time
import datetime
import pandas as pd
from dotenv import load_dotenv

if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"

load_dotenv()
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

st.set_page_config(
    page_title="ExamPrep AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #0d0d2b 50%, #0a0a1a 100%);
    color: #e2e8f0;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d2b 0%, #1a0a2e 100%);
    border-right: 1px solid rgba(139, 92, 246, 0.2);
}

.glass-card {
    background: rgba(139, 92, 246, 0.05);
    border: 1px solid rgba(139, 92, 246, 0.2);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

.glass-card:hover {
    border-color: rgba(139, 92, 246, 0.5);
    background: rgba(139, 92, 246, 0.08);
    transform: translateY(-2px);
}

.metric-card {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(59, 130, 246, 0.1));
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    transition: all 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-4px);
    border-color: rgba(139, 92, 246, 0.6);
    box-shadow: 0 8px 32px rgba(139, 92, 246, 0.2);
}

.metric-number {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #8b5cf6, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.metric-label {
    font-size: 0.85rem;
    color: #94a3b8;
    margin-top: 4px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.hero {
    text-align: center;
    padding: 60px 20px 40px;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #8b5cf6, #3b82f6, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 16px;
    line-height: 1.2;
}

.hero-subtitle {
    font-size: 1.2rem;
    color: #94a3b8;
    margin-bottom: 32px;
}

.feature-card {
    background: rgba(139, 92, 246, 0.05);
    border: 1px solid rgba(139, 92, 246, 0.15);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    margin-bottom: 12px;
}

.feature-icon { font-size: 2rem; margin-bottom: 8px; }
.feature-title { font-size: 1rem; font-weight: 600; color: #c4b5fd; margin-bottom: 4px; }
.feature-desc { font-size: 0.8rem; color: #64748b; }

.question-card {
    background: rgba(15, 15, 40, 0.8);
    border: 1px solid rgba(139, 92, 246, 0.2);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    border-left: 4px solid #8b5cf6;
}

.question-number {
    font-size: 0.75rem;
    color: #8b5cf6;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
}

.question-text {
    font-size: 1rem;
    color: #e2e8f0;
    font-weight: 500;
    line-height: 1.6;
}

.badge {
    display: inline-block;
    background: rgba(139, 92, 246, 0.2);
    border: 1px solid rgba(139, 92, 246, 0.4);
    color: #c4b5fd;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 16px;
}

.sidebar-logo { text-align: center; padding: 20px 0; }
.sidebar-logo-text {
    font-size: 1.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #8b5cf6, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sidebar-logo-sub { font-size: 0.7rem; color: #64748b; letter-spacing: 2px; text-transform: uppercase; }
.sidebar-divider { border: none; border-top: 1px solid rgba(139, 92, 246, 0.15); margin: 12px 0; }
.sidebar-section {
    font-size: 0.7rem; color: #64748b; text-transform: uppercase;
    letter-spacing: 1.5px; font-weight: 600; margin: 12px 0 8px 0;
}
.user-badge {
    padding: 8px 12px;
    background: rgba(139,92,246,0.1);
    border-radius: 8px;
    margin-bottom: 16px;
    font-size: 0.85rem;
    color: #c4b5fd;
    font-weight: 500;
}

.stButton > button {
    background: linear-gradient(135deg, #8b5cf6, #3b82f6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 16px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
    margin-bottom: 4px !important;
}

.stButton > button:hover {
    background: rgba(139, 92, 246, 0.1) !important;
    border-color: rgba(139, 92, 246, 0.4) !important;
    color: #c4b5fd !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(15, 15, 40, 0.8) !important;
    border: 1px solid rgba(139, 92, 246, 0.3) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2) !important;
}

.stProgress > div > div > div {
    background: linear-gradient(135deg, #8b5cf6, #3b82f6) !important;
}

.page-title {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #8b5cf6, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}

.page-subtitle { color: #64748b; font-size: 0.9rem; margin-bottom: 24px; }

/* Timer styles */
.timer-normal {
    font-size: 2rem; font-weight: 700; color: #8b5cf6;
    text-align: center; padding: 12px; border-radius: 12px;
    border: 2px solid rgba(139,92,246,0.3);
    background: rgba(139,92,246,0.1);
}
.timer-warning {
    font-size: 2rem; font-weight: 700; color: #f59e0b;
    text-align: center; padding: 12px; border-radius: 12px;
    border: 2px solid rgba(245,158,11,0.5);
    background: rgba(245,158,11,0.1);
    animation: pulse 1s infinite;
}
.timer-danger {
    font-size: 2rem; font-weight: 700; color: #ef4444;
    text-align: center; padding: 12px; border-radius: 12px;
    border: 2px solid rgba(239,68,68,0.5);
    background: rgba(239,68,68,0.1);
    animation: pulse 0.5s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}

/* History table */
.history-row {
    background: rgba(15,15,40,0.6);
    border: 1px solid rgba(139,92,246,0.15);
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Progress bar label */
.progress-label {
    font-size: 0.8rem; color: #94a3b8; margin-bottom: 4px;
}

section[data-testid="stSidebar"] {
    display: block !important;
    visibility: visible !important;
    width: 250px !important;
    min-width: 250px !important;
    transform: none !important;
}

[data-testid="collapsedControl"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION DEFAULTS ----------------
defaults = {
    "logged_in": False,
    "auth_page": "login",
    "current_page": "Dashboard",
    "generated": False,
    "doc_count": 0,
    "question_count": 0,
    "quiz_count": 0,
    "show_answers": False,
    "mcq": [],
    "short": [],
    "viva": [],
    "vector_store": None,
    "embedder": None,
    "chat_history": [],
    "flashcards": [],
    "card_index": 0,
    "card_flipped": False,
    "username": "",
    # New: Quiz timer
    "quiz_time_limit": 30,
    "quiz_start_time": None,
    "timed_mode": False,
    # New: Score history
    "score_history": [],
    # New: Per-type progress tracking
    "mcq_attempted": 0,
    "short_attempted": 0,
    "viva_attempted": 0,
    # Day 2: Difficulty filter
    "mcq_difficulty_filter": "All",
    # Day 2 v2: Study streak
    "streak_days": 0,
    "last_study_date": "",
    "total_study_days": 0,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ---------------- USER STORAGE ----------------
USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def login(username, password):
    users = load_users()
    return username in users and users[username] == password

def signup(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = password
    save_users(users)
    return True


# ---------------- STREAK TRACKER ----------------
def update_streak():
    """Call once per session when user does something productive (upload or quiz)."""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    last = st.session_state.last_study_date

    if last == today:
        return  # Already counted today

    if last == "":
        # First time ever
        st.session_state.streak_days = 1
    else:
        last_dt = datetime.datetime.strptime(last, "%Y-%m-%d")
        today_dt = datetime.datetime.strptime(today, "%Y-%m-%d")
        diff = (today_dt - last_dt).days
        if diff == 1:
            st.session_state.streak_days += 1   # Consecutive day
        elif diff > 1:
            st.session_state.streak_days = 1    # Streak broken

    st.session_state.last_study_date = today
    st.session_state.total_study_days += 1


# ---------------- LOGIN PAGE ----------------
def login_page():
    st.markdown("""
    <div class="hero">
        <div class="badge">Powered by LLaMA 3.3 + RAG</div>
        <div class="hero-title">ExamPrep AI</div>
        <div class="hero-subtitle">Upload your notes. Generate smart questions.<br>Chat with your PDF. Ace your exams.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    features = [
        ("🧠", "AI Questions", "MCQ, Short & Viva questions from your notes"),
        ("💬", "Chat with PDF", "Ask anything from your uploaded document"),
        ("📝", "Answer Eval", "Get AI feedback and score on your answers"),
        ("⏱️", "Timed Quiz", "Race against the clock with a timed quiz mode"),
    ]
    for col, (icon, title, desc) in zip([col1, col2, col3, col4], features):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_mid, col_right = st.columns([1, 1.2, 1])

    with col_mid:
        if st.session_state.auth_page == "login":
            st.markdown("### Welcome Back")
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Login"):
                if login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<center><small style='color:#64748b'>Don't have an account?</small></center>", unsafe_allow_html=True)
            if st.button("Create Account"):
                st.session_state.auth_page = "signup"
                st.rerun()
        else:
            st.markdown("### Create Account")
            username = st.text_input("Username", placeholder="Choose a username")
            password = st.text_input("Password", type="password", placeholder="Choose a password")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sign Up"):
                if signup(username, password):
                    st.success("Account created! Please login.")
                    st.session_state.auth_page = "login"
                    st.rerun()
                else:
                    st.error("Username already exists")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Back to Login"):
                st.session_state.auth_page = "login"
                st.rerun()


# ---------------- SIDEBAR ----------------
def sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <div class="sidebar-logo-text">ExamPrep AI</div>
            <div class="sidebar-logo-sub">Powered by LLaMA 3.3</div>
        </div>
        <hr class="sidebar-divider">
        """, unsafe_allow_html=True)

        if st.session_state.username:
            streak = st.session_state.streak_days
            streak_color = "#f59e0b" if streak >= 3 else "#94a3b8"
            st.markdown(f"""
            <div class="user-badge">👤 {st.session_state.username}</div>
            <div style="text-align:center; padding:6px 12px; background:rgba(245,158,11,0.1);
            border:1px solid rgba(245,158,11,0.2); border-radius:8px; margin-bottom:12px;
            font-size:0.85rem; color:{streak_color}; font-weight:600;">
                🔥 {streak} day streak
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section">Navigation</div>', unsafe_allow_html=True)

        pages = [
            ("Dashboard", "📊"),
            ("Upload & Generate", "📤"),
            ("Score History", "🏆"),
            ("Progress", "📈"),
        ]
        for label, icon in pages:
            key = label.split(" ")[0]
            if st.button(f"{icon} {label}"):
                st.session_state.current_page = key
                st.rerun()

        if st.session_state.generated:
            st.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)
            st.markdown('<div class="sidebar-section">Study Tools</div>', unsafe_allow_html=True)
            tools = [
                ("MCQ Questions", "MCQ", "🔵"),
                ("Short Answers", "Short", "📋"),
                ("Long Answers", "Long", "📝"),
                ("Timed Quiz", "Quiz", "⏱️"),
                ("Chat with PDF", "Chat", "💬"),
                ("Answer Evaluation", "Evaluate", "🎯"),
                ("Flashcards", "Flashcards", "🃏"),
                ("Export Questions", "Export", "⬇️"),
                ("Analytics", "Analytics", "📊"),
            ]
            for label, page, icon in tools:
                if st.button(f"{icon} {label}"):
                    st.session_state.current_page = page
                    st.rerun()

        st.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)
        st.session_state.show_answers = st.toggle("Show Answers", value=st.session_state.show_answers)
        st.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)

        if st.button("🚪 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# ---------------- MAIN APP ----------------
def main_app():
    from src.data_processing.pdf_loader import load_pdf
    from src.data_processing.cleaner import clean_text
    from src.chunking.chunker import TextChunker
    from src.embeddings.embedder import Embedder
    from src.embeddings.vector_store import VectorStore
    from src.rag.retriever import Retriever
    from src.rag.question_generator import QuestionGenerator

    sidebar()
    page = st.session_state.current_page

    # ---------------- DASHBOARD ----------------
    if page == "Dashboard":
        st.markdown(f"""
        <div class="page-title">Dashboard</div>
        <div class="page-subtitle">Welcome back, {st.session_state.username or 'Student'}! Ready to study?</div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        metrics = [
            (st.session_state.doc_count, "Documents"),
            (st.session_state.question_count, "Questions"),
            (st.session_state.quiz_count, "Quizzes"),
            (f"🔥 {st.session_state.streak_days}", "Day Streak"),
        ]
        for col, (num, label) in zip([col1, col2, col3, col4], metrics):
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-number">{num}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:1rem; font-weight:600; color:#94a3b8;
        text-transform:uppercase; letter-spacing:1px; margin-bottom:16px;">
        Quick Actions
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📤 Upload Document"):
                st.session_state.current_page = "Upload"
                st.rerun()
        with col2:
            if st.button("⏱️ Start Timed Quiz"):
                st.session_state.current_page = "Quiz"
                st.rerun()
        with col3:
            if st.button("💬 Chat with PDF"):
                st.session_state.current_page = "Chat"
                st.rerun()
        with col4:
            if st.button("🏆 Score History"):
                st.session_state.current_page = "Score History"
                st.rerun()

        # Recent score summary
        if st.session_state.score_history:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Recent Quiz Results**")
            for entry in st.session_state.score_history[-3:][::-1]:
                color = "#22c55e" if entry["accuracy"] >= 80 else "#f59e0b" if entry["accuracy"] >= 50 else "#ef4444"
                st.markdown(f"""
                <div class="history-row">
                    <span style="color:#94a3b8; font-size:0.8rem;">{entry["date"]}</span>
                    <span style="color:#e2e8f0; font-size:0.9rem;">{entry["score"]}/{entry["total"]}</span>
                    <span style="color:{color}; font-weight:700;">{entry["accuracy"]}%</span>
                    <span style="color:#64748b; font-size:0.8rem;">{'⏱️ ' + str(entry.get('time_per_q', '—')) + 's avg' if entry.get('timed') else 'Normal'}</span>
                </div>
                """, unsafe_allow_html=True)

        if not st.session_state.generated:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div class="glass-card" style="text-align:center; padding: 40px;">
                <div style="font-size: 3rem; margin-bottom: 16px;">📚</div>
                <div style="font-size: 1.1rem; color: #c4b5fd; font-weight: 600; margin-bottom: 8px;">No documents yet</div>
                <div style="font-size: 0.85rem; color: #64748b;">Upload a PDF to start generating questions with AI</div>
            </div>
            """, unsafe_allow_html=True)

    # ---------------- UPLOAD ----------------
    elif page == "Upload":
        st.markdown("""
        <div class="page-title">Upload & Generate</div>
        <div class="page-subtitle">Upload your study material and let AI generate questions for you</div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])
        with col1:
            uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
        with col2:
            num_questions = st.selectbox("Questions per type", [5, 10, 15])

        if uploaded_file:
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.read())

            raw_text = load_pdf("temp.pdf")
            cleaned_text = clean_text(raw_text)
            chunker = TextChunker()
            chunks = chunker.split_text(cleaned_text)

            st.markdown(f"""
            <div style="background: rgba(59,130,246,0.1); border: 1px solid rgba(59,130,246,0.3);
            border-radius: 10px; padding: 12px 16px; margin-bottom: 16px;
            font-size: 0.9rem; color: #93c5fd;">
            Document processed — <b>{len(chunks)} chunks</b> created and ready for embedding
            </div>
            """, unsafe_allow_html=True)

            if st.button("🚀 Generate Questions"):
                with st.spinner("Building vector index..."):
                    embedder = Embedder()
                    embeddings = embedder.embed_texts(chunks)
                    vector_store = VectorStore()
                    vector_store.add_embeddings(embeddings, chunks)
                    st.session_state.vector_store = vector_store
                    st.session_state.embedder = embedder

                with st.spinner("Retrieving most relevant content..."):
                    retriever = Retriever(vector_store, embedder)
                    relevant_chunks = retriever.retrieve(
                        query="key concepts, definitions, and important topics", top_k=5
                    )
                    context = "\n\n".join(relevant_chunks)

                with st.spinner("Generating questions with LLaMA 3.3..."):
                    try:
                        generator = QuestionGenerator()
                        mcq, short, viva = generator.generate_questions(context, num_questions)
                        st.session_state.mcq = mcq[:num_questions]
                        st.session_state.short = short[:num_questions]
                        st.session_state.viva = viva[:num_questions]
                        st.session_state.generated = True
                        st.session_state.doc_count += 1
                        st.session_state.question_count += num_questions
                        update_streak()
                        st.balloons()
                        st.success(f"✅ {num_questions * 3} questions generated successfully!")
                        st.info("Use the sidebar to explore MCQs, Timed Quiz, Flashcards and more!")
                        time.sleep(2)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.markdown("""
            <div class="glass-card" style="text-align:center; padding:40px;">
                <div style="font-size:3rem; margin-bottom:16px;">☁️</div>
                <div style="color:#c4b5fd; font-weight:600; margin-bottom:8px;">Drop your PDF here</div>
                <div style="color:#64748b; font-size:0.85rem;">Supports lecture notes, textbooks, and study material</div>
            </div>
            """, unsafe_allow_html=True)

    # ---------------- MCQ ----------------
    elif page == "MCQ":
        st.markdown("""
        <div class="page-title">MCQ Questions</div>
        <div class="page-subtitle">Multiple choice questions generated from your document</div>
        """, unsafe_allow_html=True)

        if not st.session_state.mcq:
            st.warning("No questions yet. Upload a PDF first.")
            return

        # ---------------- DIFFICULTY FILTER ----------------
        # Assign difficulty to each MCQ based on index if not already assigned
        mcq_list = st.session_state.mcq
        difficulty_labels = ["Easy", "Medium", "Hard"]
        difficulty_colors = {"Easy": "#22c55e", "Medium": "#f59e0b", "Hard": "#ef4444"}

        for i, q in enumerate(mcq_list):
            if "difficulty" not in q:
                q["difficulty"] = difficulty_labels[i % 3]

        col_filter, col_count = st.columns([2, 1])
        with col_filter:
            selected_difficulty = st.selectbox(
                "🎯 Filter by Difficulty",
                ["All", "Easy", "Medium", "Hard"],
                index=["All", "Easy", "Medium", "Hard"].index(
                    st.session_state.mcq_difficulty_filter
                )
            )
            st.session_state.mcq_difficulty_filter = selected_difficulty

        filtered_mcq = mcq_list if selected_difficulty == "All" else [
            q for q in mcq_list if q.get("difficulty") == selected_difficulty
        ]

        with col_count:
            st.markdown(f"""
            <div style="background:rgba(139,92,246,0.1); border:1px solid rgba(139,92,246,0.3);
            border-radius:10px; padding:12px; text-align:center; margin-top:4px;">
                <span style="color:#8b5cf6; font-weight:700; font-size:1.3rem;">{len(filtered_mcq)}</span>
                <span style="color:#64748b; font-size:0.8rem;"> questions</span>
            </div>
            """, unsafe_allow_html=True)

        # Difficulty count badges
        easy_c = sum(1 for q in mcq_list if q.get("difficulty") == "Easy")
        med_c  = sum(1 for q in mcq_list if q.get("difficulty") == "Medium")
        hard_c = sum(1 for q in mcq_list if q.get("difficulty") == "Hard")
        st.markdown(f"""
        <div style="margin-bottom:20px;">
            <span style="background:rgba(34,197,94,0.15); color:#22c55e; border:1px solid rgba(34,197,94,0.3);
            padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:600; margin-right:8px;">
            🟢 Easy: {easy_c}</span>
            <span style="background:rgba(245,158,11,0.15); color:#f59e0b; border:1px solid rgba(245,158,11,0.3);
            padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:600; margin-right:8px;">
            🟡 Medium: {med_c}</span>
            <span style="background:rgba(239,68,68,0.15); color:#ef4444; border:1px solid rgba(239,68,68,0.3);
            padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:600;">
            🔴 Hard: {hard_c}</span>
        </div>
        """, unsafe_allow_html=True)

        # Track how many MCQs the user viewed
        st.session_state.mcq_attempted = len(filtered_mcq)

        if not filtered_mcq:
            st.info("No questions match this difficulty filter.")
            return

        for i, q in enumerate(filtered_mcq):
            diff = q.get("difficulty", "Medium")
            diff_color = difficulty_colors[diff]
            st.markdown(f"""
            <div class="question-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div class="question-number">Question {i+1}</div>
                    <span style="background:rgba(0,0,0,0.3); color:{diff_color};
                    border:1px solid {diff_color}40; padding:2px 10px;
                    border-radius:12px; font-size:0.75rem; font-weight:600;">{diff}</span>
                </div>
                <div class="question-text">{q["question"]}</div>
            </div>
            """, unsafe_allow_html=True)
            for idx, opt in enumerate(q["options"]):
                st.write(f"{'ABCD'[idx]}. {opt}")
            if st.session_state.show_answers:
                st.success(f"✅ Answer: {q['answer']}")
            st.markdown("<hr style='border-color: rgba(139,92,246,0.1);'>", unsafe_allow_html=True)

    # ---------------- SHORT ----------------
    elif page == "Short":
        st.markdown("""
        <div class="page-title">Short Answer Questions</div>
        <div class="page-subtitle">Questions requiring brief, focused answers</div>
        """, unsafe_allow_html=True)

        if not st.session_state.short:
            st.warning("No questions yet. Upload a PDF first.")
            return

        st.session_state.short_attempted = len(st.session_state.short)

        for i, q in enumerate(st.session_state.short):
            st.markdown(f"""
            <div class="question-card">
                <div class="question-number">Question {i+1}</div>
                <div class="question-text">{q}</div>
            </div>
            """, unsafe_allow_html=True)

    # ---------------- LONG ----------------
    elif page == "Long":
        st.markdown("""
        <div class="page-title">Viva Questions</div>
        <div class="page-subtitle">Deep conceptual questions for detailed answers</div>
        """, unsafe_allow_html=True)

        if not st.session_state.viva:
            st.warning("No questions yet. Upload a PDF first.")
            return

        st.session_state.viva_attempted = len(st.session_state.viva)

        for i, q in enumerate(st.session_state.viva):
            st.markdown(f"""
            <div class="question-card">
                <div class="question-number">Question {i+1}</div>
                <div class="question-text">{q}</div>
            </div>
            """, unsafe_allow_html=True)

    # ---------------- TIMED QUIZ ----------------
    elif page == "Quiz":
        st.markdown("""
        <div class="page-title">⏱️ Timed Quiz Mode</div>
        <div class="page-subtitle">Race against the clock — answer before time runs out!</div>
        """, unsafe_allow_html=True)

        questions = st.session_state.mcq
        total = len(questions)

        if total == 0:
            st.warning("No questions yet. Please upload a PDF first.")
            return

        # Quiz setup screen
        if "q_index" not in st.session_state:
            st.session_state.q_index = 0
        if "score" not in st.session_state:
            st.session_state.score = 0

        # Show setup options if quiz hasn't started
        if st.session_state.quiz_start_time is None:
            st.markdown("""
            <div class="glass-card" style="text-align:center; padding:32px;">
                <div style="font-size:2.5rem; margin-bottom:12px;">⏱️</div>
                <div style="color:#c4b5fd; font-weight:600; font-size:1.1rem; margin-bottom:8px;">Configure Your Quiz</div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                time_limit = st.selectbox(
                    "⏳ Seconds per question",
                    [15, 20, 30, 45, 60],
                    index=2
                )
                st.session_state.quiz_time_limit = time_limit
            with col2:
                timed = st.checkbox("Enable Timer", value=True)
                st.session_state.timed_mode = timed

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 Start Quiz"):
                st.session_state.q_index = 0
                st.session_state.score = 0
                st.session_state.quiz_start_time = time.time()
                st.rerun()
            return

        # --- Active quiz ---
        q = questions[st.session_state.q_index]
        elapsed = time.time() - st.session_state.quiz_start_time
        remaining = max(0, st.session_state.quiz_time_limit - elapsed)

        # Progress bar for quiz
        progress = st.session_state.q_index / total
        st.progress(progress)
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; margin-bottom:16px;">
            <span style="color:#8b5cf6; font-weight:600;">
                Question {st.session_state.q_index + 1} of {total}
            </span>
            <span style="color:#64748b;">
                Score: {st.session_state.score}/{st.session_state.q_index}
            </span>
        </div>
        """, unsafe_allow_html=True)

        col_q, col_t = st.columns([3, 1])

        with col_q:
            st.markdown(f"""
            <div class="question-card" style="padding: 28px;">
                <div class="question-number">Question {st.session_state.q_index + 1}</div>
                <div class="question-text" style="font-size:1.1rem;">{q["question"]}</div>
            </div>
            """, unsafe_allow_html=True)
            selected = st.radio("Choose your answer:", q["options"], key=f"q_{st.session_state.q_index}")

        with col_t:
            if st.session_state.timed_mode:
                if remaining > 10:
                    timer_class = "timer-normal"
                elif remaining > 5:
                    timer_class = "timer-warning"
                else:
                    timer_class = "timer-danger"

                st.markdown(f"""
                <div style="margin-top:20px;">
                    <div class="{timer_class}">{int(remaining)}s</div>
                    <div style="text-align:center; color:#64748b; font-size:0.75rem; margin-top:8px;">
                        remaining
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Auto-advance if time runs out
                if remaining <= 0:
                    # Don't count as correct (time expired)
                    st.session_state.q_index += 1
                    st.session_state.quiz_start_time = time.time()
                    if st.session_state.q_index >= total:
                        st.session_state.current_page = "Result"
                    st.rerun()
                else:
                    time.sleep(0.5)
                    st.rerun()

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Next"):
                if selected == q["answer"]:
                    st.session_state.score += 1
                st.session_state.q_index += 1
                st.session_state.quiz_start_time = time.time()  # reset timer per question
                if st.session_state.q_index >= total:
                    st.session_state.current_page = "Result"
                st.rerun()

        with col2:
            if st.button("❌ Exit Quiz"):
                st.session_state.q_index = 0
                st.session_state.score = 0
                st.session_state.quiz_start_time = None
                st.session_state.current_page = "Dashboard"
                st.rerun()

    # ---------------- CHAT ----------------
    elif page == "Chat":
        st.markdown("""
        <div class="page-title">Chat with PDF</div>
        <div class="page-subtitle">Ask any question from your uploaded document</div>
        """, unsafe_allow_html=True)

        if not st.session_state.chat_history:
            st.markdown("""
            <div class="glass-card" style="text-align:center; padding:30px;">
                <div style="font-size:2.5rem; margin-bottom:12px;">💬</div>
                <div style="color:#c4b5fd; font-weight:600; margin-bottom:8px;">Start a conversation</div>
                <div style="color:#64748b; font-size:0.85rem;">Ask anything about your uploaded PDF document</div>
            </div>
            """, unsafe_allow_html=True)

        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat["question"])
            with st.chat_message("assistant"):
                st.write(chat["answer"])

        question = st.chat_input("Ask something from your PDF...")

        if question:
            if st.session_state.vector_store is None:
                st.warning("Please upload a PDF first!")
            else:
                retriever = Retriever(st.session_state.vector_store, st.session_state.embedder)
                relevant_chunks = retriever.retrieve(question, top_k=5)
                context = "\n\n".join(relevant_chunks)
                with st.spinner("Thinking..."):
                    generator = QuestionGenerator()
                    answer = generator.chat_with_pdf(question, context)
                st.session_state.chat_history.append({"question": question, "answer": answer})
                st.rerun()

    # ---------------- EVALUATE ----------------
    elif page == "Evaluate":
        st.markdown("""
        <div class="page-title">Answer Evaluation</div>
        <div class="page-subtitle">Write your answer and get instant AI feedback with score</div>
        """, unsafe_allow_html=True)

        if not st.session_state.short:
            st.warning("No questions yet. Upload a PDF first.")
            return

        selected_q = st.selectbox("Select a question:", st.session_state.short)
        student_answer = st.text_area("Your Answer:", placeholder="Write your answer here...", height=150)

        if st.button("🎯 Evaluate My Answer"):
            if not student_answer.strip():
                st.warning("Please write an answer first!")
            else:
                with st.spinner("Evaluating your answer..."):
                    retriever = Retriever(st.session_state.vector_store, st.session_state.embedder)
                    relevant_chunks = retriever.retrieve(selected_q, top_k=3)
                    context = "\n\n".join(relevant_chunks)
                    generator = QuestionGenerator()
                    result = generator.evaluate_answer(selected_q, student_answer, context)

                score = result.get("score", 0)
                out_of = result.get("out_of", 10)
                feedback = result.get("feedback", "")
                correct_answer = result.get("correct_answer", "")

                col1, col2 = st.columns(2)
                with col1:
                    color = "#22c55e" if score >= 8 else "#f59e0b" if score >= 5 else "#ef4444"
                    st.markdown(f"""
                    <div style="background: rgba(0,0,0,0.3); border: 2px solid {color};
                    border-radius: 16px; padding: 24px; text-align:center;">
                        <div style="font-size: 3rem; font-weight: 700; color: {color};">{score}/{out_of}</div>
                        <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 4px;">Your Score</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    percentage = (score / out_of) * 100
                    st.markdown(f"""
                    <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(139,92,246,0.3);
                    border-radius: 16px; padding: 24px; text-align:center;">
                        <div style="font-size: 3rem; font-weight: 700; color: #8b5cf6;">{round(percentage)}%</div>
                        <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 4px;">Accuracy</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("#### Feedback")
                st.info(feedback)
                st.markdown("#### Ideal Answer")
                st.success(correct_answer)

    # ---------------- FLASHCARDS ----------------
    elif page == "Flashcards":
        st.markdown("""
        <div class="page-title">Flashcards</div>
        <div class="page-subtitle">Flip through key concepts from your document</div>
        """, unsafe_allow_html=True)

        if not st.session_state.flashcards:
            if st.button("🃏 Generate Flashcards"):
                with st.spinner("Generating flashcards..."):
                    retriever = Retriever(st.session_state.vector_store, st.session_state.embedder)
                    relevant_chunks = retriever.retrieve(
                        query="key concepts, definitions, and important terms", top_k=5
                    )
                    context = "\n\n".join(relevant_chunks)
                    generator = QuestionGenerator()
                    st.session_state.flashcards = generator.generate_flashcards(context, num=10)
                    st.session_state.card_index = 0
                    st.session_state.card_flipped = False
                    st.rerun()
        else:
            cards = st.session_state.flashcards
            total = len(cards)
            idx = st.session_state.card_index
            card = cards[idx]

            st.progress((idx + 1) / total)
            st.markdown(f"""
            <div style="text-align:center; color:#64748b; font-size:0.85rem; margin-bottom:24px;">
                Card {idx + 1} of {total}
            </div>
            """, unsafe_allow_html=True)

            if not st.session_state.card_flipped:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(139,92,246,0.15), rgba(59,130,246,0.1));
                border: 2px solid rgba(139,92,246,0.4); border-radius: 20px; padding: 60px 40px;
                text-align: center; min-height: 250px; margin-bottom: 24px;">
                    <div style="font-size:0.75rem; color:#8b5cf6; font-weight:600;
                    text-transform:uppercase; letter-spacing:2px; margin-bottom:20px;">Front</div>
                    <div style="font-size:1.4rem; font-weight:600; color:#e2e8f0; line-height:1.5;">
                        {card["front"]}
                    </div>
                    <div style="font-size:0.8rem; color:#64748b; margin-top:24px;">
                        Click "Flip Card" to see the answer
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(34,197,94,0.1), rgba(59,130,246,0.1));
                border: 2px solid rgba(34,197,94,0.4); border-radius: 20px; padding: 60px 40px;
                text-align: center; min-height: 250px; margin-bottom: 24px;">
                    <div style="font-size:0.75rem; color:#22c55e; font-weight:600;
                    text-transform:uppercase; letter-spacing:2px; margin-bottom:20px;">Back</div>
                    <div style="font-size:1.1rem; color:#e2e8f0; line-height:1.7;">
                        {card["back"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                if idx > 0:
                    if st.button("⬅️ Previous"):
                        st.session_state.card_index -= 1
                        st.session_state.card_flipped = False
                        st.rerun()
            with col2:
                if not st.session_state.card_flipped:
                    if st.button("🔄 Flip Card"):
                        st.session_state.card_flipped = True
                        st.rerun()
                else:
                    if st.button("🔄 Flip Back"):
                        st.session_state.card_flipped = False
                        st.rerun()
            with col3:
                if idx < total - 1:
                    if st.button("➡️ Next"):
                        st.session_state.card_index += 1
                        st.session_state.card_flipped = False
                        st.rerun()
                else:
                    if st.button("🔁 Restart"):
                        st.session_state.card_index = 0
                        st.session_state.card_flipped = False
                        st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("♻️ Generate New Flashcards"):
                st.session_state.flashcards = []
                st.session_state.card_index = 0
                st.session_state.card_flipped = False
                st.rerun()

    # ---------------- SCORE HISTORY ----------------
    elif page == "Score History":
        st.markdown("""
        <div class="page-title">🏆 Score History</div>
        <div class="page-subtitle">Track your quiz performance over time</div>
        """, unsafe_allow_html=True)

        history = st.session_state.score_history

        if not history:
            st.markdown("""
            <div class="glass-card" style="text-align:center; padding:40px;">
                <div style="font-size:3rem; margin-bottom:16px;">📊</div>
                <div style="color:#c4b5fd; font-weight:600; margin-bottom:8px;">No quiz history yet</div>
                <div style="color:#64748b; font-size:0.85rem;">Complete a quiz to see your results here</div>
            </div>
            """, unsafe_allow_html=True)
            return

        # Summary stats
        total_quizzes = len(history)
        avg_acc = round(sum(e["accuracy"] for e in history) / total_quizzes)
        best = max(history, key=lambda x: x["accuracy"])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">{total_quizzes}</div>
                <div class="metric-label">Total Quizzes</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">{avg_acc}%</div>
                <div class="metric-label">Avg Accuracy</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">{best["accuracy"]}%</div>
                <div class="metric-label">Best Score</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**All Quiz Results**")

        for i, entry in enumerate(reversed(history)):
            color = "#22c55e" if entry["accuracy"] >= 80 else "#f59e0b" if entry["accuracy"] >= 50 else "#ef4444"
            timed_tag = f"⏱️ {entry.get('time_per_q', '—')}s/q" if entry.get("timed") else "Normal Mode"
            st.markdown(f"""
            <div class="history-row">
                <span style="color:#64748b; font-size:0.8rem;">#{len(history) - i}</span>
                <span style="color:#94a3b8; font-size:0.8rem;">{entry["date"]}</span>
                <span style="color:#e2e8f0;">{entry["score"]}/{entry["total"]}</span>
                <span style="color:{color}; font-weight:700; font-size:1.1rem;">{entry["accuracy"]}%</span>
                <span style="color:#64748b; font-size:0.75rem;">{timed_tag}</span>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🗑️ Clear History"):
            st.session_state.score_history = []
            st.rerun()

    # ---------------- PROGRESS ----------------
    elif page == "Progress":
        st.markdown("""
        <div class="page-title">📈 Progress Tracker</div>
        <div class="page-subtitle">See how much you've studied across all question types</div>
        """, unsafe_allow_html=True)

        total_mcq = len(st.session_state.mcq)
        total_short = len(st.session_state.short)
        total_viva = len(st.session_state.viva)

        types = [
            ("MCQ Questions", st.session_state.mcq_attempted, total_mcq, "#8b5cf6"),
            ("Short Answers", st.session_state.short_attempted, total_short, "#3b82f6"),
            ("Viva Questions", st.session_state.viva_attempted, total_viva, "#06b6d4"),
        ]

        for label, done, total, color in types:
            pct = int((done / total) * 100) if total > 0 else 0
            st.markdown(f"""
            <div class="glass-card">
                <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                    <span style="font-weight:600; color:#e2e8f0;">{label}</span>
                    <span style="color:{color}; font-weight:700;">{pct}%</span>
                </div>
                <div style="background:rgba(255,255,255,0.05); border-radius:8px; height:10px; overflow:hidden;">
                    <div style="background:{color}; width:{pct}%; height:100%; border-radius:8px;
                    transition:width 0.5s ease;"></div>
                </div>
                <div style="color:#64748b; font-size:0.8rem; margin-top:6px;">{done} of {total} reviewed</div>
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.score_history:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Quiz Accuracy Trend**")
            accuracy_data = [e["accuracy"] for e in st.session_state.score_history]
            st.line_chart(accuracy_data)

    # ---------------- EXPORT ----------------
    elif page == "Export":
        st.markdown("""
        <div class="page-title">⬇️ Export Questions</div>
        <div class="page-subtitle">Download your generated questions as a text file</div>
        """, unsafe_allow_html=True)

        if not st.session_state.generated:
            st.warning("No questions yet. Upload a PDF first.")
            return

        export_format = st.selectbox("Select format", ["Plain Text (.txt)", "Markdown (.md)"])

        lines = []

        if st.session_state.mcq:
            lines.append("=" * 50)
            lines.append("MCQ QUESTIONS")
            lines.append("=" * 50)
            for i, q in enumerate(st.session_state.mcq):
                lines.append(f"\nQ{i+1}. {q['question']}")
                for idx, opt in enumerate(q["options"]):
                    lines.append(f"   {'ABCD'[idx]}. {opt}")
                lines.append(f"   Answer: {q['answer']}")

        if st.session_state.short:
            lines.append("\n" + "=" * 50)
            lines.append("SHORT ANSWER QUESTIONS")
            lines.append("=" * 50)
            for i, q in enumerate(st.session_state.short):
                lines.append(f"\nQ{i+1}. {q}")

        if st.session_state.viva:
            lines.append("\n" + "=" * 50)
            lines.append("VIVA / LONG ANSWER QUESTIONS")
            lines.append("=" * 50)
            for i, q in enumerate(st.session_state.viva):
                lines.append(f"\nQ{i+1}. {q}")

        content = "\n".join(lines)

        ext = ".txt" if "Text" in export_format else ".md"
        fname = f"ExamPrep_Questions{ext}"

        st.download_button(
            label=f"⬇️ Download {fname}",
            data=content,
            file_name=fname,
            mime="text/plain"
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Preview:**")
        st.code(content[:1000] + ("..." if len(content) > 1000 else ""), language="markdown")

    # ---------------- ANALYTICS ----------------
    elif page == "Analytics":
        st.markdown("""
        <div class="page-title">📊 Analytics</div>
        <div class="page-subtitle">Detailed breakdown of your study performance</div>
        """, unsafe_allow_html=True)

        history = st.session_state.score_history

        if not history:
            st.markdown("""
            <div class="glass-card" style="text-align:center; padding:40px;">
                <div style="font-size:3rem; margin-bottom:16px;">📊</div>
                <div style="color:#c4b5fd; font-weight:600; margin-bottom:8px;">No data yet</div>
                <div style="color:#64748b; font-size:0.85rem;">Complete at least one quiz to see analytics</div>
            </div>
            """, unsafe_allow_html=True)
            return

        # ---- Top summary cards ----
        total_q = sum(e["total"] for e in history)
        total_correct = sum(e["score"] for e in history)
        avg_acc = round(sum(e["accuracy"] for e in history) / len(history))
        timed_quizzes = sum(1 for e in history if e.get("timed"))

        col1, col2, col3, col4 = st.columns(4)
        for col, (num, label) in zip(
            [col1, col2, col3, col4],
            [
                (len(history), "Total Quizzes"),
                (f"{avg_acc}%", "Avg Accuracy"),
                (total_correct, "Correct Answers"),
                (timed_quizzes, "Timed Quizzes"),
            ]
        ):
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-number">{num}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ---- Accuracy trend chart ----
        st.markdown("**📈 Accuracy Over Time**")
        acc_data = {"Quiz #": list(range(1, len(history) + 1)),
                    "Accuracy (%)": [e["accuracy"] for e in history]}
        df_acc = pd.DataFrame(acc_data).set_index("Quiz #")
        st.line_chart(df_acc)

        st.markdown("<br>", unsafe_allow_html=True)

        # ---- Score breakdown bar chart ----
        st.markdown("**📊 Score vs Total Per Quiz**")
        df_scores = pd.DataFrame({
            "Correct": [e["score"] for e in history],
            "Wrong": [e["total"] - e["score"] for e in history],
        }, index=[f"Q{i+1}" for i in range(len(history))])
        st.bar_chart(df_scores)

        st.markdown("<br>", unsafe_allow_html=True)

        # ---- Timed vs Normal breakdown ----
        timed_acc = [e["accuracy"] for e in history if e.get("timed")]
        normal_acc = [e["accuracy"] for e in history if not e.get("timed")]

        col_t, col_n = st.columns(2)
        with col_t:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;">
                <div style="font-size:1.5rem; margin-bottom:8px;">⏱️</div>
                <div style="color:#8b5cf6; font-weight:700; font-size:1.8rem;">
                    {round(sum(timed_acc)/len(timed_acc)) if timed_acc else "—"}{'%' if timed_acc else ''}
                </div>
                <div style="color:#64748b; font-size:0.8rem; margin-top:4px;">
                    Avg accuracy in Timed Mode ({len(timed_acc)} quizzes)
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_n:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;">
                <div style="font-size:1.5rem; margin-bottom:8px;">🧘</div>
                <div style="color:#3b82f6; font-weight:700; font-size:1.8rem;">
                    {round(sum(normal_acc)/len(normal_acc)) if normal_acc else "—"}{'%' if normal_acc else ''}
                </div>
                <div style="color:#64748b; font-size:0.8rem; margin-top:4px;">
                    Avg accuracy in Normal Mode ({len(normal_acc)} quizzes)
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ---- Study streak info ----
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding:28px;">
            <div style="font-size:2.5rem; margin-bottom:8px;">🔥</div>
            <div style="font-size:1.8rem; font-weight:700; color:#f59e0b;">
                {st.session_state.streak_days} day streak
            </div>
            <div style="color:#64748b; font-size:0.85rem; margin-top:4px;">
                {st.session_state.total_study_days} total days studied
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- RESULT ----------------
    elif page == "Result":
        total = len(st.session_state.mcq)
        score = st.session_state.score
        accuracy = round((score / total) * 100) if total > 0 else 0

        color = "#22c55e" if accuracy >= 80 else "#f59e0b" if accuracy >= 50 else "#ef4444"
        emoji = "🔥" if accuracy >= 80 else "📈" if accuracy >= 50 else "📚"

        # Save to history
        time_per_q = st.session_state.quiz_time_limit if st.session_state.timed_mode else None
        st.session_state.score_history.append({
            "date": datetime.datetime.now().strftime("%d %b %Y, %H:%M"),
            "score": score,
            "total": total,
            "accuracy": accuracy,
            "timed": st.session_state.timed_mode,
            "time_per_q": time_per_q,
        })
        st.session_state.quiz_count += 1
        st.session_state.quiz_start_time = None
        update_streak()

        st.markdown(f"""
        <div style="text-align:center; padding: 60px 20px;">
            <div style="font-size: 4rem; margin-bottom: 16px;">{emoji}</div>
            <div style="font-size: 2.5rem; font-weight: 700; color: {color}; margin-bottom: 8px;">
                {score} / {total}
            </div>
            <div style="font-size: 1.1rem; color: #94a3b8; margin-bottom: 32px;">
                You scored {accuracy}% accuracy
                {' — Timed Mode ⏱️' if st.session_state.timed_mode else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if accuracy >= 80:
            st.success("🔥 Excellent! You are very well prepared!")
        elif accuracy >= 50:
            st.info("📈 Good effort! Review weak areas and try again.")
        else:
            st.warning("📚 Keep practicing! Read the material again.")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔁 Try Again"):
                st.session_state.q_index = 0
                st.session_state.score = 0
                st.session_state.quiz_start_time = None
                st.session_state.current_page = "Quiz"
                st.rerun()
        with col2:
            if st.button("🏆 View History"):
                st.session_state.current_page = "Score History"
                st.rerun()
        with col3:
            if st.button("🏠 Dashboard"):
                st.session_state.q_index = 0
                st.session_state.score = 0
                st.session_state.current_page = "Dashboard"
                st.rerun()


# ---------------- ROUTING ----------------
if not st.session_state.logged_in:
    login_page()
else:
    main_app()