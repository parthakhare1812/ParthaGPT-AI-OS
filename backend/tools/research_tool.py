from backend.tools.web_search import (
    web_search
)

# -----------------------------
# AI RESEARCH TOOL
# -----------------------------

def research_topic(query):

    web_results = web_search(
        query
    )

    formatted_results = f"""
LIVE WEB RESEARCH RESULTS:

{web_results}
"""

    return formatted_results