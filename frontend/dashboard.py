import streamlit as st

from memory_viewer import load_memories
from reflection_viewer import load_reflections
from workflow_viewer import get_workflows
from agent_monitor import get_agent_status

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="ParthaGPT Dashboard",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown(
    """
<style>

.main {
    background-color: white;
    color: black;
}

.block {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #d1d5db;
    margin-bottom: 20px;
    background-color: #f8fafc;
}

</style>
""",
    unsafe_allow_html=True
)

# -----------------------------
# TITLE
# -----------------------------

st.title("🧠 ParthaGPT Autonomous Dashboard")

st.markdown(
    """
Monitor memories, reflections, workflows, and autonomous AI agents.
"""
)

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("⚡ System Overview")

st.sidebar.markdown(
    """
### Active Systems

- Semantic Memory
- Reflection Engine
- Multi-Agent System
- Workflow Engine
- Background Agents
- Tool-Using Agents
- Web Intelligence
"""
)

# -----------------------------
# MEMORY SECTION
# -----------------------------

st.header("📚 Memory System")

memories = load_memories()

st.write(f"Total Memories: {len(memories)}")

for memory in memories[-5:]:

    with st.expander(memory["file"]):

        st.write(memory["content"])

# -----------------------------
# REFLECTION SECTION
# -----------------------------

st.header("🪞 Reflection Engine")

reflections = load_reflections()

st.write(f"Total Reflections: {len(reflections)}")

for reflection in reflections[-3:]:

    with st.expander(reflection["file"]):

        st.write(reflection["content"])

# -----------------------------
# WORKFLOW SECTION
# -----------------------------

st.header("⚙️ Autonomous Workflows")

workflows = get_workflows()

for workflow in workflows:

    st.markdown(
        f"""
<div class="block">
<b>{workflow['name']}</b><br>
Status: {workflow['status']}
</div>
""",
        unsafe_allow_html=True
    )

# -----------------------------
# AGENT SECTION
# -----------------------------

st.header("🤖 Active Agents")

agents = get_agent_status()

for agent in agents:

    st.markdown(
        f"""
<div class="block">
<b>{agent['agent']}</b><br>
Status: {agent['status']}
</div>
""",
        unsafe_allow_html=True
    )

# -----------------------------
# FOOTER
# -----------------------------

st.markdown(
    "---"
)

st.markdown(
    """
### ParthaGPT AI Operating Platform

Persistent Autonomous Intelligence System
"""
)