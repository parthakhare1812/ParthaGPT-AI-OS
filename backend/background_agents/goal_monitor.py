from backend.goal_engine import (
    generate_goal_insights
)

# -----------------------------
# RUN GOAL MONITOR
# -----------------------------

def run_goal_monitor():

    insights = generate_goal_insights()

    print("\n===== GOAL MONITOR =====\n")

    print(insights)

    return insights