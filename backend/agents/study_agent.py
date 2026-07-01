"""
study_agent.py
--------------
Study Agent for ParthaGPT-AI-OS.

This agent provides structured learning and study recommendations
based on the user's query.  It follows the same simple function-based
pattern used by all other agents in the system — the returned text is
injected into the main Groq prompt as additional multi-agent context
(see backend/agents/router.py and backend/chatbot.py).

Author: SSoC 2026 contributor
"""


def study_agent(query: str) -> str:
    """Return structured study and learning recommendations for a given query.

    The Study Agent helps the user plan effective learning sessions,
    choose the right resources, and apply memory-science techniques
    (e.g. spaced repetition, active recall) to any topic they want to
    learn about.

    Unlike agents that call an LLM directly, this agent returns a
    formatted string that is concatenated with output from other agents
    and passed as context to the central Groq LLM call in chatbot.py.

    Args:
        query (str): The user's raw input message.  The agent uses this
                     to personalise its recommendations so the Groq LLM
                     can refer back to the original question.

    Returns:
        str: A multi-line string beginning with "[Study Agent]" that
             contains actionable study tips and the original query for
             context.

    Example:
        >>> result = study_agent("How do I learn Python quickly?")
        >>> result.startswith("[Study Agent]")
        True
        >>> "Python" in result
        True
    """
    # Build the response using an f-string so the original query is
    # echoed back — this lets the LLM understand which specific topic
    # the study recommendations are referring to.
    return f"""
[Study Agent]

Study & Learning Recommendations:
- Break complex topics into small, focused 25-minute study sessions (Pomodoro technique)
- Use active recall: after reading, close the material and write down what you remember
- Apply spaced repetition: review new concepts after 1 day, 3 days, 1 week, and 1 month
- Build real projects around every concept you learn — hands-on practice beats passive reading
- Teach back the concept in your own words to identify gaps in your understanding
- Prioritise first-principles understanding over memorising syntax or steps
- Keep a daily learning log to track progress and spot patterns in what you find difficult

Relevant Query:
{query}
"""
