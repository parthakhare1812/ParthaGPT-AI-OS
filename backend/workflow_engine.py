from backend.tools.research_tool import (
    research_topic
)

from backend.tools.project_generator import (
    generate_project_plan
)

from backend.goal_engine import (
    generate_goal_insights
)

# -----------------------------
# GENERATE WORKFLOW
# -----------------------------

def generate_workflow(query):

    query = query.lower()

    # -----------------------------
    # STARTUP WORKFLOW
    # -----------------------------

    if "startup" in query:

        return [
            "research",
            "project_plan",
            "goal_analysis"
        ]

    # -----------------------------
    # PROJECT WORKFLOW
    # -----------------------------

    elif any(word in query for word in [
        "project",
        "build",
        "system"
    ]):

        return [
            "research",
            "project_plan"
        ]

    # -----------------------------
    # CAREER WORKFLOW
    # -----------------------------

    elif any(word in query for word in [
        "career",
        "roadmap",
        "improve"
    ]):

        return [
            "goal_analysis",
            "research"
        ]

    # -----------------------------
    # DEFAULT
    # -----------------------------

    return [
        "research"
    ]

# -----------------------------
# EXECUTE WORKFLOW
# -----------------------------

def execute_workflow(query):

    workflow_steps = generate_workflow(
        query
    )

    workflow_results = []

    # -----------------------------
    # STEP EXECUTION
    # -----------------------------

    for step in workflow_steps:

        # -----------------------------
        # RESEARCH
        # -----------------------------

        if step == "research":

            result = research_topic(
                query
            )

            workflow_results.append(
                f"""
[RESEARCH STEP]

{result}
"""
            )

        # -----------------------------
        # PROJECT PLAN
        # -----------------------------

        elif step == "project_plan":

            result = generate_project_plan(
                query
            )

            workflow_results.append(
                f"""
[PROJECT PLAN STEP]

{result}
"""
            )

        # -----------------------------
        # GOAL ANALYSIS
        # -----------------------------

        elif step == "goal_analysis":

            result = generate_goal_insights()

            workflow_results.append(
                f"""
[GOAL ANALYSIS STEP]

{result}
"""
            )

    # -----------------------------
    # FINAL OUTPUT
    # -----------------------------

    final_workflow_output = "\n\n".join(
        workflow_results
    )

    return final_workflow_output