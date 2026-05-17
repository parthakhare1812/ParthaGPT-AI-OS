# -----------------------------
# TASK DETECTION
# -----------------------------

def detect_task_type(query):

    query = query.lower()

    if any(word in query for word in [
        "roadmap",
        "plan",
        "strategy",
        "improve"
    ]):

        return "planning"

    elif any(word in query for word in [
        "startup",
        "business",
        "idea",
        "monetize"
    ]):

        return "startup"

    elif any(word in query for word in [
        "learn",
        "study",
        "skill",
        "career"
    ]):

        return "learning"

    elif any(word in query for word in [
        "build",
        "project",
        "system",
        "architecture"
    ]):

        return "project_execution"

    return "general"

# -----------------------------
# EXECUTION PLANNER
# -----------------------------

def generate_execution_plan(task_type):

    plans = {

        "planning": [
            "Analyze current position",
            "Identify gaps",
            "Create roadmap",
            "Suggest improvements"
        ],

        "startup": [
            "Generate startup idea",
            "Analyze market potential",
            "Design MVP",
            "Suggest monetization"
        ],

        "learning": [
            "Analyze current skills",
            "Identify weak areas",
            "Create learning roadmap",
            "Suggest practice systems"
        ],

        "project_execution": [
            "Analyze project idea",
            "Suggest architecture",
            "Recommend tech stack",
            "Create implementation roadmap"
        ],

        "general": [
            "Analyze query",
            "Generate intelligent response"
        ]
    }

    return plans.get(
        task_type,
        plans["general"]
    )

# -----------------------------
# EXECUTE TASK
# -----------------------------

def execute_task(query):

    task_type = detect_task_type(
        query
    )

    execution_steps = generate_execution_plan(
        task_type
    )

    formatted_plan = f"""
TASK TYPE:
{task_type}

EXECUTION PLAN:
"""

    for index, step in enumerate(
        execution_steps,
        start=1
    ):

        formatted_plan += f"""
{index}. {step}
"""

    return formatted_plan