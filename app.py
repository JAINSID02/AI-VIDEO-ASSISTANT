import streamlit as st
import os
import sys

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Google Fonts + Global CSS ──────────────────────────────────────────────────
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">

    <style>
    /* ── Reset & base ── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background: #000 !important;
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stHeader"] { background: transparent !important; }
    [data-testid="stSidebar"] { display: none; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    section[data-testid="stMain"] > div { padding: 0 !important; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: #0A0A0A; }
    ::-webkit-scrollbar-thumb { background: #8B5CF6; border-radius: 2px; }

    /* ── Hero ── */
    .hero {
        width: 100%;
        padding: 64px 24px 48px;
        text-align: center;
        position: relative;
        overflow: hidden;
        background: #000;
    }
    .hero::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse 70% 50% at 50% 0%, rgba(139,92,246,0.15) 0%, transparent 70%);
        pointer-events: none;
    }

    /* Waveform bars */
    .waveform {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 3px;
        height: 40px;
        margin-bottom: 28px;
    }
    .wave-bar {
        width: 3px;
        background: #8B5CF6;
        border-radius: 2px;
        animation: wave 1.4s ease-in-out infinite;
        opacity: 0.85;
    }
    .wave-bar:nth-child(1)  { height: 14px; animation-delay: 0.0s; }
    .wave-bar:nth-child(2)  { height: 22px; animation-delay: 0.1s; }
    .wave-bar:nth-child(3)  { height: 32px; animation-delay: 0.2s; }
    .wave-bar:nth-child(4)  { height: 38px; animation-delay: 0.3s; }
    .wave-bar:nth-child(5)  { height: 28px; animation-delay: 0.4s; }
    .wave-bar:nth-child(6)  { height: 40px; animation-delay: 0.5s; }
    .wave-bar:nth-child(7)  { height: 30px; animation-delay: 0.4s; }
    .wave-bar:nth-child(8)  { height: 38px; animation-delay: 0.3s; }
    .wave-bar:nth-child(9)  { height: 22px; animation-delay: 0.2s; }
    .wave-bar:nth-child(10) { height: 14px; animation-delay: 0.1s; }

    @keyframes wave {
        0%, 100% { transform: scaleY(0.5); opacity: 0.5; }
        50%       { transform: scaleY(1.0); opacity: 1.0; }
    }

    .hero-eyebrow {
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        color: #8B5CF6;
        margin-bottom: 14px;
    }
    .hero-title {
        font-family: 'Cinzel', serif;
        font-size: clamp(32px, 5vw, 60px);
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1.1;
        letter-spacing: 0.01em;
        margin-bottom: 14px;
    }
    .hero-title span { color: #8B5CF6; }
    .hero-subtitle {
        font-size: 15px;
        font-weight: 300;
        color: #94A3B8;
        max-width: 480px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* ── Divider ── */
    .divider {
        width: 100%;
        height: 1px;
        background: linear-gradient(90deg, transparent, #8B5CF620, #8B5CF6, #8B5CF620, transparent);
        margin: 0;
    }

    /* ── Main panel ── */
    .main-panel {
        max-width: 820px;
        margin: 0 auto;
        padding: 48px 24px 80px;
    }

    /* ── Input card ── */
    .input-card {
        background: #0D0D0D;
        border: 1px solid #1E1E2E;
        border-radius: 12px;
        padding: 28px 28px 24px;
        margin-bottom: 32px;
    }
    .input-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #64748B;
        margin-bottom: 10px;
    }

    /* Streamlit widget overrides */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div {
        background: #000 !important;
        border: 1px solid #1E1E2E !important;
        border-radius: 8px !important;
        color: #E2E8F0 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        padding: 10px 14px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 0 2px rgba(139,92,246,0.2) !important;
    }
    .stSelectbox > div > div > div:focus-within {
        border-color: #8B5CF6 !important;
    }
    div[data-baseweb="select"] > div {
        background: #000 !important;
        border-color: #1E1E2E !important;
    }
    div[data-baseweb="popover"] { background: #0D0D0D !important; }
    li[role="option"] { color: #E2E8F0 !important; background: #0D0D0D !important; }
    li[role="option"]:hover { background: #1E1E2E !important; }

    /* ── Button ── */
    .stButton > button {
        background: linear-gradient(135deg, #7C3AED, #8B5CF6) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        letter-spacing: 0.08em !important;
        padding: 10px 28px !important;
        cursor: pointer !important;
        transition: opacity 0.2s !important;
        text-transform: uppercase !important;
    }
    .stButton > button:hover { opacity: 0.85 !important; }
    .stButton > button:active { opacity: 0.7 !important; }

    /* ── Result card ── */
    .result-section {
        background: #0D0D0D;
        border: 1px solid #1E1E2E;
        border-radius: 12px;
        margin-bottom: 16px;
        overflow: hidden;
    }
    .result-header {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 16px 20px;
        border-bottom: 1px solid #1E1E2E;
    }
    .result-icon {
        width: 28px;
        height: 28px;
        border-radius: 6px;
        background: rgba(139,92,246,0.15);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
    }
    .result-title {
        font-family: 'Cinzel', serif;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #C4B5FD;
    }
    .result-body {
        padding: 18px 20px;
        font-size: 14px;
        font-weight: 300;
        line-height: 1.75;
        color: #CBD5E1;
    }
    .result-body ul { padding-left: 18px; }
    .result-body li { margin-bottom: 6px; }

    /* Transcript (collapsible) */
    .stExpander {
        background: #0D0D0D !important;
        border: 1px solid #1E1E2E !important;
        border-radius: 12px !important;
        margin-bottom: 16px !important;
    }
    .stExpander summary {
        color: #C4B5FD !important;
        font-family: 'Cinzel', serif !important;
        font-size: 12px !important;
        letter-spacing: 0.12em !important;
        font-weight: 600 !important;
    }

    /* ── Chat section ── */
    .chat-header {
        font-family: 'Cinzel', serif;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #8B5CF6;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid #1E1E2E;
    }
    .chat-bubble {
        padding: 12px 16px;
        border-radius: 10px;
        margin-bottom: 10px;
        font-size: 14px;
        line-height: 1.6;
        max-width: 88%;
    }
    .chat-bubble.user {
        background: rgba(139,92,246,0.15);
        border: 1px solid rgba(139,92,246,0.25);
        color: #E2E8F0;
        margin-left: auto;
    }
    .chat-bubble.assistant {
        background: #111;
        border: 1px solid #1E1E2E;
        color: #CBD5E1;
    }
    .chat-name {
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .chat-name.user { color: #8B5CF6; text-align: right; }
    .chat-name.assistant { color: #64748B; }

    /* Spinner */
    .stSpinner > div { border-top-color: #8B5CF6 !important; }

    /* Info / error */
    .stAlert { background: #0D0D0D !important; border-color: #1E1E2E !important; color: #94A3B8 !important; border-radius: 10px !important; }

    /* Label text color */
    label, .stTextInput label, .stSelectbox label { color: #64748B !important; font-size: 12px !important; }

    /* Footer */
    .footer {
        text-align: center;
        padding: 24px;
        font-size: 11px;
        color: #1E293B;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <div class="waveform">
            <div class="wave-bar"></div><div class="wave-bar"></div>
            <div class="wave-bar"></div><div class="wave-bar"></div>
            <div class="wave-bar"></div><div class="wave-bar"></div>
            <div class="wave-bar"></div><div class="wave-bar"></div>
            <div class="wave-bar"></div><div class="wave-bar"></div>
        </div>
        <p class="hero-eyebrow">Powered by AI</p>
        <h1 class="hero-title">AI <span>Video</span> Assistant</h1>
        <p class="hero-subtitle">
            Transcribe, summarize, and converse with any video or audio source —
            YouTube links or local files.
        </p>
    </div>
    <div class="divider"></div>
    """,
    unsafe_allow_html=True,
)

# ── Session state ──────────────────────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "processing" not in st.session_state:
    st.session_state.processing = False

# ── Main panel ────────────────────────────────────────────────────────────────
st.markdown('<div class="main-panel">', unsafe_allow_html=True)

# Input card
st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown('<p class="input-label">Source</p>', unsafe_allow_html=True)

source = st.text_input(
    label="source_input",
    placeholder="Paste a YouTube URL or enter a local file path…",
    label_visibility="collapsed",
)

col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    language = st.selectbox(
        "Language",
        ["english", "hinglish", "hindi"],
        label_visibility="visible",
    )
with col3:
    st.markdown("<div style='margin-top:26px'></div>", unsafe_allow_html=True)
    run_btn = st.button("▶  Analyse", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn and source:
    st.session_state.chat_history = []
    with st.spinner("Processing your video — this may take a moment…"):
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from dotenv import load_dotenv
            load_dotenv()
            from main import run_pipeline
            st.session_state.result = run_pipeline(source, language)
        except Exception as e:
            st.error(f"Something went wrong: {e}")

elif run_btn and not source:
    st.warning("Please enter a YouTube URL or local file path.")

# ── Results ──────────────────────────────────────────────────────────────────
if st.session_state.result:
    r = st.session_state.result

    # Title badge
    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom:28px;">
            <div style="display:inline-block; background:rgba(139,92,246,0.1);
                border:1px solid rgba(139,92,246,0.3); border-radius:8px;
                padding:10px 24px;">
                <span style="font-family:'Cinzel',serif; font-size:15px;
                    font-weight:600; color:#C4B5FD;">{r.get('title','Untitled')}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Cards
    def result_card(icon, title, content_html):
        st.markdown(
            f"""
            <div class="result-section">
                <div class="result-header">
                    <div class="result-icon">{icon}</div>
                    <span class="result-title">{title}</span>
                </div>
                <div class="result-body">{content_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    result_card("📋", "Summary", f"<p>{r.get('summary','')}</p>")

    def list_html(items):
        if isinstance(items, list):
            return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
        return f"<p>{items}</p>"

    result_card("✅", "Action Items", list_html(r.get("action_item", [])))
    result_card("🏛", "Key Decisions", list_html(r.get("key_decisions", [])))
    result_card("❓", "Open Questions", list_html(r.get("questions", [])))

    # Transcript collapsible
    with st.expander("📄  Full Transcript"):
        st.markdown(
            f"<div style='font-size:13px;line-height:1.8;color:#94A3B8;'>{r.get('transcript','')}</div>",
            unsafe_allow_html=True,
        )

    # ── Chat ──────────────────────────────────────────────────────────────────
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="chat-header">💬 &nbsp; Chat with Your Video</div>', unsafe_allow_html=True)

    # Render history
    for msg in st.session_state.chat_history:
        role = msg["role"]
        bubble_class = "user" if role == "user" else "assistant"
        name = "You" if role == "user" else "Assistant"
        st.markdown(
            f"""
            <div class="chat-name {bubble_class}">{name}</div>
            <div class="chat-bubble {bubble_class}">{msg['content']}</div>
            """,
            unsafe_allow_html=True,
        )

    # Input row
    q_col, send_col = st.columns([5, 1])
    with q_col:
        user_q = st.text_input(
            "Ask a question",
            placeholder="Ask anything about the video…",
            label_visibility="collapsed",
            key="chat_input",
        )
    with send_col:
        send_btn = st.button("Send", use_container_width=True)

    if send_btn and user_q:
        from core.rag_engine import ask_question
        with st.spinner("Thinking…"):
            answer = ask_question(r["rag_chain"], user_q)
        st.session_state.chat_history.append({"role": "user", "content": user_q})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)  # close main-panel

# Footer
st.markdown(
    '<div class="footer">AI Video Assistant &nbsp;·&nbsp; Built with Streamlit</div>',
    unsafe_allow_html=True,
)