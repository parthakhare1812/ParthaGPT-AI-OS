from backend.tools.memory_inspector import (
    inspect_memory
)

from backend.tools.project_generator import (
    generate_project_plan
)

from backend.tools.research_tool import (
    research_topic
)

# -----------------------------
# TOOL ROUTER
# -----------------------------

def run_tools(query):

    query_lower = query.lower()

    tool_outputs = []

    # -----------------------------
    # MEMORY TOOL
    # -----------------------------

    if "memory" in query_lower:

        memory_output = inspect_memory(
            query
        )

        tool_outputs.append(
            memory_output
        )

    # -----------------------------
    # PROJECT TOOL
    # -----------------------------

    if any(word in query_lower for word in [
        "project",
        "build",
        "system"
    ]):

        project_output = generate_project_plan(
            query
        )

        tool_outputs.append(
            project_output
        )

    # -----------------------------
    # WEB RESEARCH TOOL
    # -----------------------------

    if any(word in query_lower for word in [
        "latest",
        "trend",
        "research",
        "news",
        "technology",
        "ai trend"
    ]):

        research_output = research_topic(
            query
        )

        tool_outputs.append(
            research_output
        )

    # -----------------------------
    # NO TOOL
    # -----------------------------

    if len(tool_outputs) == 0:

        return "No tools triggered."

    return "\n\n".join(
        tool_outputs
    )