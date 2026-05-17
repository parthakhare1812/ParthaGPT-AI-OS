from backend.tools.research_tool import (
    research_topic
)

# -----------------------------
# RUN TREND MONITOR
# -----------------------------

def run_trend_monitor():

    query = """
latest AI agent trends
autonomous AI systems
advanced RAG architectures
"""

    trends = research_topic(
        query
    )

    print("\n===== TREND MONITOR =====\n")

    print(trends)

    return trends