from backend.agents.strategist_agent import (
    strategist_agent
)

from backend.agents.coding_agent import (
    coding_agent
)

from backend.agents.research_agent import (
    research_agent
)

from backend.agents.creativity_agent import (
    creativity_agent
)

from backend.agents.career_agent import (
    career_agent
)

# -----------------------------
# RUN MULTI AGENT SYSTEM
# -----------------------------

def run_agents(query):

    strategist = strategist_agent(query)

    coder = coding_agent(query)

    researcher = research_agent(query)

    creativity = creativity_agent(query)

    career = career_agent(query)

    combined_output = f"""
{strategist}

{coder}

{researcher}

{creativity}

{career}
"""

    return combined_output