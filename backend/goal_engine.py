from backend.retriever import retrieve_memory

# -----------------------------
# ANALYZE GOALS
# -----------------------------

def analyze_goals():

    # Retrieve goal-related memories

    goal_memories = retrieve_memory(
        "career goals future ambitions learning roadmap",
        top_k=10
    )

    goals_context = "\n\n".join(
        goal_memories
    )

    return goals_context

# -----------------------------
# GENERATE GOAL INSIGHTS
# -----------------------------

def generate_goal_insights():

    goals_context = analyze_goals()

    insights = f"""
STRATEGIC GOAL ANALYSIS

Based on stored goals and memories:

{goals_context}

Potential Focus Areas:
- AI engineering growth
- autonomous systems
- scalable architecture
- deployment improvement
- advanced RAG systems
- multi-agent systems

Recommended Strategic Direction:
Focus on combining:
- AI systems
- memory architectures
- automation
- scalable engineering
- intelligent workflows

Potential Skill Gaps:
- production deployment
- large-scale architecture
- advanced backend scalability
- AI orchestration systems

Growth Pattern:
Strong project-building mindset with increasing focus on futuristic AI systems.
"""

    return insights