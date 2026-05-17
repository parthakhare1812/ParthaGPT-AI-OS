import time

import streamlit as st

from streamlit_option_menu import option_menu

from backend.chatbot import ask_parthagpt

from frontend.memory_viewer import (
    load_memories
)

from frontend.reflection_viewer import (
    load_reflections
)

from frontend.workflow_viewer import (
    get_workflows
)

from frontend.agent_monitor import (
    get_agent_status
)

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="ParthaGPT AI OS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown(
    """
<style>

/* Main App */
.stApp {
    background-color: #0f172a;
    color: white;
}

/* Sidebar Text */
.css-1d391kg,
.css-163ttbj,
.css-10trblm,
.css-qrbaxs {
    color: #f8fafc !important;
    font-weight: 600 !important;
}

/* Titles */
h1, h2, h3 {
    color: #f8fafc;
}

/* Cards */
.glow-card {
    background: rgba(17, 24, 39, 0.85);
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 0 15px rgba(59, 130, 246, 0.15);
}

/* Chat User */
.user-message {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    padding: 16px;
    border-radius: 16px;
    margin-bottom: 12px;
    color: white;
}

/* Chat AI */
.ai-message {
    background: #1e293b;
    padding: 16px;
    border-radius: 16px;
    margin-bottom: 22px;
    border: 1px solid #334155;
    color: #f8fafc;
}

/* Analytics */
.metric-card {
    background: #111827;
    padding: 18px;
    border-radius: 16px;
    text-align: center;
    border: 1px solid #1e40af;
    box-shadow: 0 0 12px rgba(59,130,246,0.12);
}

/* Thinking */
.thinking-box {
    background: #111827;
    border-left: 4px solid #38bdf8;
    padding: 14px;
    border-radius: 10px;
    margin-bottom: 10px;
}

</style>
""",
    unsafe_allow_html=True
)

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------

with st.sidebar:

    st.markdown(
        """
# 🧠 ParthaGPT
### Autonomous AI OS
"""
    )

    selected = option_menu(
        menu_title=None,

        options=[
            "Chat",
            "Memory",
            "Reflections",
            "Agents",
            "Workflows",
            "Analytics"
        ],

        icons=[
            "chat-dots",
            "database",
            "eye",
            "cpu",
            "diagram-3",
            "bar-chart"
        ],

        default_index=0,

        styles={
            "container": {
                "background-color": "#111827"
            },

            "icon": {
                "color": "#38bdf8",
                "font-size": "18px"
            },

            "nav-link": {
                    "color": "#f8fafc",
                    "font-size": "18px",
                    "font-weight": "600",
                    "text-align": "left",
                    "margin": "8px",
                    "padding": "12px",
                    "border-radius": "12px",
                    "--hover-color": "#1e293b"
                },

            "nav-link-selected": {
                    "background-color": "#2563eb",
                    "color": "white",
                    "font-weight": "700",
                    "box-shadow": "0 0 12px rgba(37,99,235,0.6)"
                }
        }
    )

    st.markdown("---")

    st.markdown(
        """
### ⚡ AI SYSTEMS

✅ Semantic Memory

✅ Reflection Engine

✅ Multi-Agent System

✅ Workflow Engine

✅ Web Intelligence

✅ Background Agents
"""
    )

# -----------------------------
# HEADER
# -----------------------------

st.title("🚀 ParthaGPT AI Operating System")

st.caption(
    "Persistent Autonomous Multi-Agent Intelligence Platform"
)

# -----------------------------
# ANALYTICS BAR
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown(
        """
<div class="metric-card">
<h3>Memories</h3>
<h2>248</h2>
</div>
""",
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        """
<div class="metric-card">
<h3>Agents</h3>
<h2>5</h2>
</div>
""",
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        """
<div class="metric-card">
<h3>Workflows</h3>
<h2>31</h2>
</div>
""",
        unsafe_allow_html=True
    )

with col4:

    st.markdown(
        """
<div class="metric-card">
<h3>Status</h3>
<h2>ACTIVE</h2>
</div>
""",
        unsafe_allow_html=True
    )

st.markdown("---")

# -----------------------------
# CHAT PAGE
# -----------------------------

if selected == "Chat":

    st.subheader("💬 Autonomous AI Chat")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_query = st.text_input(
        "Enter your command or question"
    )

    if st.button("Run AI System"):

        if user_query.strip() != "":

            # -----------------------------
            # THINKING STATES
            # -----------------------------

            thinking_placeholder = st.empty()

            thinking_steps = [
                "🧠 Retrieving semantic memories...",
                "⚡ Running multi-agent reasoning...",
                "🌐 Accessing web intelligence...",
                "🪞 Generating reflective insights...",
                "🚀 Executing workflows..."
            ]

            for step in thinking_steps:

                thinking_placeholder.markdown(
                    f"""
<div class="thinking-box">
{step}
</div>
""",
                    unsafe_allow_html=True
                )

                time.sleep(0.7)

            # -----------------------------
            # AI RESPONSE
            # -----------------------------

            response = ask_parthagpt(
                user_query
            )

            thinking_placeholder.empty()

            st.session_state.chat_history.append(
                {
                    "user": user_query,
                    "ai": response
                }
            )

    # -----------------------------
    # DISPLAY CHAT
    # -----------------------------

    for chat in reversed(
        st.session_state.chat_history
    ):

        st.markdown(
            f"""
<div class="user-message">
<b>YOU</b><br><br>
{chat['user']}
</div>
""",
            unsafe_allow_html=True
        )

        # -----------------------------
        # STREAMING EFFECT
        # -----------------------------

        streamed_text = ""

        ai_placeholder = st.empty()

        words = chat['ai'].split()

        for word in words:

            streamed_text += word + " "

            ai_placeholder.markdown(
                f"""
<div class="ai-message">
<b>PARTHAGPT</b><br><br>
{streamed_text}
</div>
""",
                unsafe_allow_html=True
            )

            time.sleep(0.01)

# -----------------------------
# MEMORY PAGE
# -----------------------------

elif selected == "Memory":

    st.subheader("📚 Semantic Memory System")

    memories = load_memories()

    st.write(
        f"Total Memory Files: {len(memories)}"
    )

    for memory in reversed(memories[-10:]):

        st.markdown(
            f"""
<div class="glow-card">
<h4>{memory['file']}</h4>
<pre>{memory['content'][:1200]}</pre>
</div>
""",
            unsafe_allow_html=True
        )

# -----------------------------
# REFLECTION PAGE
# -----------------------------

elif selected == "Reflections":

    st.subheader("🪞 Reflection Engine")

    reflections = load_reflections()

    for reflection in reversed(reflections[-5:]):

        st.markdown(
            f"""
<div class="glow-card">
<h4>{reflection['file']}</h4>
<pre>{reflection['content']}</pre>
</div>
""",
            unsafe_allow_html=True
        )

# -----------------------------
# AGENTS PAGE
# -----------------------------

elif selected == "Agents":

    st.subheader("🤖 Autonomous Agents")

    agents = get_agent_status()

    for agent in agents:

        st.markdown(
            f"""
<div class="glow-card">
<h4>{agent['agent']}</h4>
<p>Status: {agent['status']}</p>
<p>Mode: ACTIVE</p>
</div>
""",
            unsafe_allow_html=True
        )

# -----------------------------
# WORKFLOW PAGE
# -----------------------------

elif selected == "Workflows":

    st.subheader("⚙️ Workflow Engine")

    workflows = get_workflows()

    for workflow in workflows:

        st.markdown(
            f"""
<div class="glow-card">
<h4>{workflow['name']}</h4>
<p>Status: {workflow['status']}</p>
<p>Execution Layer: Autonomous</p>
</div>
""",
            unsafe_allow_html=True
        )

# -----------------------------
# ANALYTICS PAGE
# -----------------------------

elif selected == "Analytics":

    st.subheader("📊 AI Observability")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
<div class="glow-card">
<h3>Memory Retrieval Health</h3>
<p>Semantic Search: ACTIVE</p>
<p>Chunking Engine: HEALTHY</p>
<p>Reflection Layer: ACTIVE</p>
</div>
""",
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
<div class="glow-card">
<h3>Autonomous Systems</h3>
<p>Workflow Engine: RUNNING</p>
<p>Web Intelligence: CONNECTED</p>
<p>Background Agents: ACTIVE</p>
</div>
""",
            unsafe_allow_html=True
        )

# -----------------------------
# FOOTER
# -----------------------------

st.markdown("---")

st.markdown(
    """
### 🧠 ParthaGPT AI Operating Platform

Persistent Autonomous Multi-Agent Intelligence Infrastructure
"""
)