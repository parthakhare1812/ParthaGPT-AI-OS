"""
router.py
---------
Multi-Agent Router for ParthaGPT-AI-OS.

This module orchestrates all specialist agents by calling each one in
sequence with the same user query and merging their outputs into a
single string.  The combined output is then injected as "MULTI AGENT
ANALYSIS" context into the main Groq prompt inside chatbot.py.

Agents available:
    - Strategist  : long-term AI engineering strategy
    - Coding      : technical and architecture suggestions
    - Research    : state-of-the-art research insights
    - Creativity  : novel ideas and product imagination
    - Career      : career growth recommendations
    - Study       : learning strategies and study planning

Author: SSoC 2026 contributor (Study Agent added)
"""

from backend.agents.strategist_agent import strategist_agent
from backend.agents.coding_agent import coding_agent
from backend.agents.research_agent import research_agent
from backend.agents.creativity_agent import creativity_agent
from backend.agents.career_agent import career_agent
from backend.agents.study_agent import study_agent  # ← newly added agent

# -----------------------------
# RUN MULTI AGENT SYSTEM
# -----------------------------


def run_agents(query: str) -> str:
    """Run all specialist agents and return their combined output.

    Each agent is called with the same user query.  Their individual
    responses are concatenated with blank lines as separators so the
    downstream Groq LLM receives clearly delimited sections of context.

    Args:
        query (str): The raw user message to pass to every agent.

    Returns:
        str: A multi-line string containing the labelled output of every
             agent (e.g. "[Strategist Agent] …", "[Study Agent] …", etc.).

    Example:
        >>> output = run_agents("How should I learn machine learning?")
        >>> "[Study Agent]" in output
        True
        >>> "[Strategist Agent]" in output
        True
    """
    # Call each specialist agent with the user query.
    # Each function returns a pre-formatted string (no LLM call happens
    # here — the LLM is called once in chatbot.py after all context is
    # assembled).
    strategist = strategist_agent(query)
    coder = coding_agent(query)
    researcher = research_agent(query)
    creativity = creativity_agent(query)
    career = career_agent(query)
    study = study_agent(query)  # ← newly added

    # Join all agent outputs with blank lines so they are easy to read
    # in the assembled prompt.
    combined_output = f"""
{strategist}

{coder}

{researcher}

{creativity}

{career}

{study}
"""

    return combined_output
