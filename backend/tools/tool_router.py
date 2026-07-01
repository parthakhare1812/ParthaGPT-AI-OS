"""
tool_router.py
--------------
Tool Router for ParthaGPT-AI-OS.

This module inspects the user's query and triggers the appropriate
tool(s) based on keyword matching.  All tool outputs are collected into
a list and joined as a single string, which is then injected as
"TOOL OUTPUTS" context into the main Groq prompt in chatbot.py.

Tools available:
    - Memory Inspector   : search ChromaDB for relevant past memories
    - Project Generator  : create a structured project roadmap
    - Research Tool      : live web research on a topic
    - Summarization Tool : condense a block of text into key sentences

Keyword triggers:
    - "memory"                                 → Memory Inspector
    - "project", "build", "system"             → Project Generator
    - "latest", "trend", "research", "news",
      "technology", "ai trend"                 → Research Tool
    - "summarize", "summarise", "summary",
      "tldr", "brief", "condense"              → Summarization Tool

Author: SSoC 2026 contributor (Summarization Tool added)
"""

from backend.tools.memory_inspector import inspect_memory
from backend.tools.project_generator import generate_project_plan
from backend.tools.research_tool import research_topic
from backend.tools.summarization_tool import summarize_text  # ← newly added

# ---------------------------------------------------------------------------
# Keywords that trigger the summarization tool.
# Using a tuple so it can be passed directly to str.startswith / "in" checks.
# ---------------------------------------------------------------------------
_SUMMARIZATION_KEYWORDS: tuple = (
    "summarize",
    "summarise",
    "summary",
    "tldr",
    "brief",
    "condense",
)

# ---------------------------------------------------------------------------
# TOOL ROUTER
# ---------------------------------------------------------------------------


def run_tools(query: str) -> str:
    """Inspect the query and run any matching tools, returning their output.

    The function checks the lower-cased query against predefined keyword
    lists for each tool.  Multiple tools can be triggered in a single
    call if the query matches more than one keyword set.

    Args:
        query (str): The raw user message to route to the appropriate
                     tool(s).

    Returns:
        str: The concatenated output of every triggered tool, separated
             by blank lines.  Returns ``"No tools triggered."`` when no
             keywords match.

    Example:
        >>> output = run_tools("Can you summarize this for me?")
        >>> "[Summary Tool]" in output
        True

        >>> output = run_tools("Good morning!")
        >>> output
        'No tools triggered.'
    """
    # Work with a lowercase copy so keyword matching is case-insensitive.
    query_lower = query.lower()

    # Collect the string output of every tool that fires.
    tool_outputs = []

    # ------------------------------------------------------------------
    # MEMORY TOOL
    # Trigger when the user asks about memory or past conversations.
    # ------------------------------------------------------------------
    if "memory" in query_lower:
        memory_output = inspect_memory(query)
        tool_outputs.append(memory_output)

    # ------------------------------------------------------------------
    # PROJECT TOOL
    # Trigger when the user wants to plan or build something.
    # ------------------------------------------------------------------
    if any(word in query_lower for word in ["project", "build", "system"]):
        project_output = generate_project_plan(query)
        tool_outputs.append(project_output)

    # ------------------------------------------------------------------
    # WEB RESEARCH TOOL
    # Trigger when the user asks for current information or trends.
    # ------------------------------------------------------------------
    if any(word in query_lower for word in [
        "latest",
        "trend",
        "research",
        "news",
        "technology",
        "ai trend",
    ]):
        research_output = research_topic(query)
        tool_outputs.append(research_output)

    # ------------------------------------------------------------------
    # SUMMARIZATION TOOL
    # Trigger when the user wants a shorter version of something.
    # We pass the query itself as the text to summarise so the tool
    # always receives a non-empty string.
    # ------------------------------------------------------------------
    if any(keyword in query_lower for keyword in _SUMMARIZATION_KEYWORDS):
        summary_output = summarize_text(query, num_sentences=3)
        tool_outputs.append(summary_output)

    # ------------------------------------------------------------------
    # NO TOOL TRIGGERED
    # Return a clear sentinel string so chatbot.py can detect this case.
    # ------------------------------------------------------------------
    if not tool_outputs:
        return "No tools triggered."

    # Join multiple tool outputs with blank lines for readability.
    return "\n\n".join(tool_outputs)
