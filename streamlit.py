import streamlit as st
import requests
import os
import time

# ─────────────────────────────────────────────
#  Page config  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="RAG App",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Dark gradient background ── */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(16px);
    border-right: 1px solid rgba(255,255,255,0.08);
}
section[data-testid="stSidebar"] * {color: #e2e8f0 !important;}

/* ── Main hero title ── */
.hero-title {
    font-size: 2.6rem;
    font-weight: 700;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.25rem;
}
.hero-sub {
    color: #94a3b8;
    font-size: 1rem;
    margin-bottom: 2rem;
}

/* ── Glass cards ── */
.glass-card {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 16px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1.25rem;
    transition: box-shadow 0.3s ease;
}
.glass-card:hover {
    box-shadow: 0 8px 32px rgba(167,139,250,0.15);
}

/* ── Step badges ── */
.step-badge {
    display: inline-block;
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    color: #fff !important;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    padding: 3px 10px;
    border-radius: 999px;
    margin-bottom: 0.55rem;
    text-transform: uppercase;
}

/* ── Section headings ── */
.section-title {
    color: #e2e8f0;
    font-size: 1.15rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
}

/* ── Status chips ── */
.chip-success {
    display:inline-block;
    background:rgba(52,211,153,0.18);
    border:1px solid rgba(52,211,153,0.35);
    color:#34d399;
    padding:4px 12px;
    border-radius:999px;
    font-size:0.82rem;
    font-weight:600;
}
.chip-error {
    display:inline-block;
    background:rgba(248,113,113,0.18);
    border:1px solid rgba(248,113,113,0.35);
    color:#f87171;
    padding:4px 12px;
    border-radius:999px;
    font-size:0.82rem;
    font-weight:600;
}
.chip-info {
    display:inline-block;
    background:rgba(96,165,250,0.18);
    border:1px solid rgba(96,165,250,0.35);
    color:#60a5fa;
    padding:4px 12px;
    border-radius:999px;
    font-size:0.82rem;
    font-weight:600;
}

/* ── Chat bubbles ── */
.chat-user {
    background: linear-gradient(135deg, #7c3aed22, #4f46e522);
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 14px 14px 4px 14px;
    padding: 0.75rem 1rem;
    margin: 0.5rem 0;
    color: #e2e8f0;
    text-align: right;
}
.chat-bot {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 14px 14px 14px 4px;
    padding: 0.75rem 1rem;
    margin: 0.5rem 0;
    color: #e2e8f0;
    text-align: left;
}
.chat-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.07em;
    margin-bottom: 0.3rem;
    text-transform: uppercase;
    color: #94a3b8;
}

/* ── Metric boxes ── */
.metric-box {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #a78bfa;
}
.metric-label {
    font-size: 0.78rem;
    color: #94a3b8;
    margin-top: 0.2rem;
}

/* ── Streamlit widget overrides ── */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}
div[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.04) !important;
    border: 2px dashed rgba(167,139,250,0.35) !important;
    border-radius: 12px !important;
}
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.5rem !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(124,58,237,0.45) !important;
}

/* ── Divider ── */
hr {border-color: rgba(255,255,255,0.08);}

/* ── Scrollbar ── */
::-webkit-scrollbar {width: 6px;}
::-webkit-scrollbar-thumb {background: rgba(167,139,250,0.4); border-radius: 3px;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Constants
# ─────────────────────────────────────────────
API_BASE = "http://127.0.0.1:8000"


# ─────────────────────────────────────────────
#  Session state
# ─────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []        # list of {"role": "user"|"bot", "text": str}
if "chunks_count" not in st.session_state:
    st.session_state.chunks_count = 0
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "processing_done" not in st.session_state:
    st.session_state.processing_done = False


# ─────────────────────────────────────────────
#  Helper: call API
# ─────────────────────────────────────────────
def api_upload(file_obj):
    try:
        r = requests.post(
            f"{API_BASE}/upload",
            files={"file": (file_obj.name, file_obj.getvalue(), file_obj.type)},
            timeout=30,
        )
        return r.status_code, r.json()
    except requests.ConnectionError:
        return 503, {"detail": "Cannot reach the backend. Is the FastAPI server running?"}
    except Exception as e:
        return 500, {"detail": str(e)}


def api_process():
    try:
        r = requests.get(f"{API_BASE}/process", timeout=600)
        return r.status_code, r.json()
    except requests.ConnectionError:
        return 503, {"detail": "Cannot reach the backend. Is the FastAPI server running?"}
    except Exception as e:
        return 500, {"detail": str(e)}


def api_ask(question: str):
    try:
        r = requests.get(
            f"{API_BASE}/ask",
            params={"question": question},
            timeout=120,
        )
        return r.status_code, r.text
    except requests.ConnectionError:
        return 503, "Cannot reach the backend. Is the FastAPI server running?"
    except Exception as e:
        return 500, str(e)


def api_delete():
    try:
        r = requests.delete(f"{API_BASE}/delete", timeout=30)
        return r.status_code, r.json()
    except requests.ConnectionError:
        return 503, {"message": "Cannot reach the backend. Is the FastAPI server running?"}
    except Exception as e:
        return 500, {"message": str(e)}


def api_health():
    try:
        r = requests.get(f"{API_BASE}/docs", timeout=5)
        return r.status_code == 200
    except Exception:
        return False


# ─────────────────────────────────────────────
#  Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 RAG App")
    st.markdown("---")

    # Backend health
    is_alive = api_health()
    status_html = (
        '<span class="chip-success">● Backend Online</span>'
        if is_alive
        else '<span class="chip-error">● Backend Offline</span>'
    )
    st.markdown(status_html, unsafe_allow_html=True)
    st.markdown("")

    # Navigation
    page = st.radio(
        "Navigate",
        ["💬 Chat", "📄 Documents", "⚙️ Settings"],
        label_visibility="collapsed",
    )
    st.markdown("---")

    # Stats
    st.markdown("### 📊 Session Stats")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(
            f'<div class="metric-box"><div class="metric-value">{len(st.session_state.chat_history)//2}</div>'
            f'<div class="metric-label">Questions Asked</div></div>',
            unsafe_allow_html=True,
        )
    with col_b:
        st.markdown(
            f'<div class="metric-box"><div class="metric-value">{st.session_state.chunks_count}</div>'
            f'<div class="metric-label">Chunks Indexed</div></div>',
            unsafe_allow_html=True,
        )
    st.markdown("")
    st.markdown(
        f'<div class="metric-box"><div class="metric-value">{len(st.session_state.uploaded_files)}</div>'
        f'<div class="metric-label">Files Uploaded This Session</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown('<span style="color:#64748b;font-size:0.78rem;">Built with Streamlit · FastAPI · Pinecone · Gemini</span>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  PAGE: Chat
# ═══════════════════════════════════════════════════════════════
if page == "💬 Chat":
    st.markdown('<div class="hero-title">Ask Your Documents</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Powered by hybrid retrieval · cross-encoder reranking · Gemini 2.5 Flash</div>', unsafe_allow_html=True)

    # Chat history display
    if not st.session_state.chat_history:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:3rem;">
            <div style="font-size:3rem;margin-bottom:1rem;">💭</div>
            <div style="color:#94a3b8;font-size:1rem;">
                No conversation yet.<br>Upload & process your documents, then ask a question below.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(
                        f'<div class="chat-user"><div class="chat-label">You</div>{msg["text"]}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div class="chat-bot"><div class="chat-label">🧠 RAG Answer</div>{msg["text"]}</div>',
                        unsafe_allow_html=True,
                    )

    st.markdown("---")

    # Input row
    col_q, col_send = st.columns([5, 1])
    with col_q:
        question = st.text_input(
            "Ask a question",
            placeholder="e.g. What are the key findings in the report?",
            label_visibility="collapsed",
            key="question_input",
        )
    with col_send:
        send = st.button("Send ➤", use_container_width=True)

    if send and question.strip():
        with st.spinner("🔍 Retrieving & generating answer…"):
            status, answer = api_ask(question.strip())

        if status == 200:
            # Strip surrounding quotes from the JSON string if present
            clean_answer = answer.strip().strip('"').replace("\\n", "\n")
            st.session_state.chat_history.append({"role": "user", "text": question.strip()})
            st.session_state.chat_history.append({"role": "bot", "text": clean_answer})
        else:
            st.error(f"❌ Error {status}: {answer}")

        st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑️ Clear Conversation"):
            st.session_state.chat_history = []
            st.rerun()


# ═══════════════════════════════════════════════════════════════
#  PAGE: Documents
# ═══════════════════════════════════════════════════════════════
elif page == "📄 Documents":
    st.markdown('<div class="hero-title">Document Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Upload, index, and manage your knowledge base</div>', unsafe_allow_html=True)

    # ── Step 1: Upload ────────────────────────────────────────
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<span class="step-badge">Step 1</span>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📤 Upload Documents</div>', unsafe_allow_html=True)
    st.markdown('<span style="color:#94a3b8;font-size:0.85rem;">Accepted formats: PDF · TXT &nbsp;|&nbsp; Max size: 10 MB per file</span>', unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Drop files here",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploaded:
        if st.button("⬆️ Upload to Server", use_container_width=False):
            results = []
            progress = st.progress(0)
            for i, f in enumerate(uploaded):
                with st.spinner(f"Uploading {f.name}…"):
                    status, resp = api_upload(f)
                    results.append((f.name, status, resp))
                    if f.name not in st.session_state.uploaded_files:
                        st.session_state.uploaded_files.append(f.name)
                progress.progress((i + 1) / len(uploaded))
            progress.empty()

            for name, status, resp in results:
                if status == 200:
                    st.markdown(f'<span class="chip-success">✓ {name} — {resp.get("message","OK")}</span><br>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<span class="chip-error">✗ {name} — {resp.get("detail","Error")}</span><br>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Step 2: Process ───────────────────────────────────────
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<span class="step-badge">Step 2</span>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚙️ Process & Index Documents</div>', unsafe_allow_html=True)
    st.markdown(
        '<span style="color:#94a3b8;font-size:0.85rem;">'
        'Chunk all uploaded files and upsert them into Pinecone. '
        'This may take a while for large document sets due to embedding rate limits.'
        '</span>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    if st.button("🚀 Process Documents", use_container_width=False):
        with st.spinner("🔄 Chunking & indexing… (this can take several minutes)"):
            status, resp = api_process()
        if status == 200:
            chunks = resp.get("chunks", 0)
            st.session_state.chunks_count = chunks
            st.session_state.processing_done = True
            st.markdown(
                f'<span class="chip-success">✓ {resp.get("message","Done")} — {chunks} chunks indexed</span>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<span class="chip-error">✗ Error {status}: {resp.get("detail", resp)}</span>',
                unsafe_allow_html=True,
            )

    if st.session_state.processing_done:
        st.markdown(
            f'<span class="chip-info">ℹ️ Last run produced {st.session_state.chunks_count} chunks</span>',
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Uploaded files list ───────────────────────────────────
    if st.session_state.uploaded_files:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📁 Files Uploaded This Session</div>', unsafe_allow_html=True)
        for fname in st.session_state.uploaded_files:
            ext = fname.rsplit(".", 1)[-1].upper()
            icon = "📕" if ext == "PDF" else "📄"
            st.markdown(f"&nbsp;&nbsp;{icon} `{fname}`", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  PAGE: Settings
# ═══════════════════════════════════════════════════════════════
elif page == "⚙️ Settings":
    st.markdown('<div class="hero-title">Settings & Danger Zone</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Configure backend connection and manage data</div>', unsafe_allow_html=True)

    # ── Backend URL ───────────────────────────────────────────
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔌 Backend Connection</div>', unsafe_allow_html=True)

    new_base = st.text_input(
        "FastAPI base URL",
        value=API_BASE,
        help="The base URL where your FastAPI server is running.",
    )
    col_check, _ = st.columns([1, 3])
    with col_check:
        if st.button("Check Connection"):
            alive = api_health()
            if alive:
                st.markdown('<span class="chip-success">✓ Backend is reachable</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="chip-error">✗ Cannot reach backend</span>', unsafe_allow_html=True)

    st.markdown(
        '<span style="color:#64748b;font-size:0.8rem;">Note: Changing the URL above requires restarting the app to take effect.</span>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Danger zone ───────────────────────────────────────────
    st.markdown('<div class="glass-card" style="border-color:rgba(248,113,113,0.25);">', unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="color:#f87171;">🗑️ Danger Zone</div>', unsafe_allow_html=True)
    st.markdown(
        '<span style="color:#94a3b8;font-size:0.85rem;">'
        'Deletes <strong style="color:#f87171;">all</strong> saved documents from disk '
        '<em>and</em> wipes the Pinecone index. This action is irreversible.'
        '</span>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    confirm = st.checkbox("I understand this will permanently delete all data")
    if confirm:
        if st.button("🔥 Delete All Data", use_container_width=False):
            with st.spinner("Deleting…"):
                status, resp = api_delete()
            if status == 200:
                st.session_state.uploaded_files = []
                st.session_state.chunks_count = 0
                st.session_state.processing_done = False
                st.markdown(f'<span class="chip-success">✓ {resp.get("message","Deleted")}</span>', unsafe_allow_html=True)
            else:
                st.markdown(f'<span class="chip-error">✗ {resp.get("message","Error")}</span>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── How to run ────────────────────────────────────────────
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📖 How to Run</div>', unsafe_allow_html=True)
    st.markdown("""
```bash
# 1. Start the FastAPI backend (from the src/ directory)
cd src
uvicorn main:app --reload --port 8000

# 2. In a separate terminal, start this Streamlit UI (from the project root)
streamlit run streamlit.py
```
    """)
    st.markdown('</div>', unsafe_allow_html=True)
