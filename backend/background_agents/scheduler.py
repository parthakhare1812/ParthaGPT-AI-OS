import time

from backend.background_agents.goal_monitor import (
    run_goal_monitor
)

from backend.background_agents.trend_monitor import (
    run_trend_monitor
)

from backend.background_agents.reflection_monitor import (
    run_reflection_monitor
)

# -----------------------------
# RUN ALL AGENTS
# -----------------------------

def run_background_agents():

    print("\n===== BACKGROUND AGENTS STARTED =====\n")

    while True:

        # -----------------------------
        # GOAL MONITOR
        # -----------------------------

        run_goal_monitor()

        # -----------------------------
        # TREND MONITOR
        # -----------------------------

        run_trend_monitor()

        # -----------------------------
        # REFLECTION MONITOR
        # -----------------------------

        run_reflection_monitor()

        # -----------------------------
        # WAIT
        # -----------------------------

        print("\nSleeping for 1 hour...\n")

        time.sleep(3600)

# -----------------------------
# START SYSTEM
# -----------------------------

if __name__ == "__main__":

    run_background_agents()