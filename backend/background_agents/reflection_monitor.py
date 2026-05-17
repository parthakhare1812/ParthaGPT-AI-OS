from backend.reflection_engine import (
    generate_reflection
)

# -----------------------------
# RUN REFLECTION MONITOR
# -----------------------------

def run_reflection_monitor():

    reflection = generate_reflection()

    print("\n===== REFLECTION MONITOR =====\n")

    print(reflection)

    return reflection