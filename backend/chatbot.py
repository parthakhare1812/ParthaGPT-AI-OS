import os

from groq import Groq
from dotenv import load_dotenv

from backend.retriever import retrieve_memory
from backend.prompts import SYSTEM_PROMPT

from backend.memory_manager import (
    save_conversation
)

from backend.live_ingest import (
    add_memory
)

from backend.personality_engine import (
    detect_personality_mode
)

from backend.goal_engine import (
    generate_goal_insights
)

from backend.agents.router import (
    run_agents
)

from backend.task_engine import (
    execute_task
)

from backend.tools.tool_router import (
    run_tools
)

from backend.workflow_engine import (
    execute_workflow
)

# -----------------------------
# LOAD ENV VARIABLES
# -----------------------------

load_dotenv()

# -----------------------------
# INITIALIZE GROQ CLIENT
# -----------------------------

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# -----------------------------
# MAIN CHAT FUNCTION
# -----------------------------

def ask_parthagpt(user_query):

    # -----------------------------
    # RETRIEVE MEMORY
    # -----------------------------

    memories = retrieve_memory(
        user_query
    )

    memory_context = "\n\n".join(
        memories
    )

    # -----------------------------
    # GOAL INSIGHTS
    # -----------------------------

    goal_insights = generate_goal_insights()

    # -----------------------------
    # MULTI-AGENT ANALYSIS
    # -----------------------------

    agent_analysis = run_agents(
        user_query
    )

    # -----------------------------
    # AUTONOMOUS TASK EXECUTION
    # -----------------------------

    task_execution = execute_task(
        user_query
    )

    # -----------------------------
    # TOOL EXECUTION
    # -----------------------------

    tool_results = run_tools(
        user_query
    )

    # -----------------------------
    # AUTONOMOUS WORKFLOW EXECUTION
    # -----------------------------

    workflow_results = execute_workflow(
        user_query
    )

    # -----------------------------
    # DETECT PERSONALITY MODE
    # -----------------------------

    personality = detect_personality_mode(
        user_query
    )

    # -----------------------------
    # FINAL PROMPT
    # -----------------------------

    final_prompt = f"""
{SYSTEM_PROMPT}

CURRENT PERSONALITY MODE:
{personality['mode']}

TONE:
{personality['tone']}

RESPONSE STYLE:
{personality['style']}

MEMORY CONTEXT:
{memory_context}

GOAL INSIGHTS:
{goal_insights}

MULTI AGENT ANALYSIS:
{agent_analysis}

AUTONOMOUS TASK EXECUTION:
{task_execution}

TOOL RESULTS:
{tool_results}

AUTONOMOUS WORKFLOW RESULTS:
{workflow_results}

USER QUESTION:
{user_query}

IMPORTANT INSTRUCTIONS:
- Adapt personality dynamically
- Use retrieved memories naturally
- Use multi-agent reasoning intelligently
- Think step-by-step when solving tasks
- Use workflow results intelligently
- Use tool outputs intelligently
- Provide execution-oriented responses
- Combine strategic + technical + creative thinking
- Keep responses personalized
- Maintain ParthaGPT identity
- Be futuristic and structured
- Think like an advanced AI strategist
- Avoid generic chatbot responses
- Provide deep reasoning where useful
- Behave like an autonomous AI system

Respond now.
"""

    # -----------------------------
    # GENERATE RESPONSE
    # -----------------------------

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": final_prompt
            }
        ],

        temperature=0.7,

        max_tokens=1500
    )

    ai_response = response.choices[0].message.content

    # -----------------------------
    # SAVE CONVERSATION
    # -----------------------------

    save_conversation(
        user_query,
        ai_response
    )

    # -----------------------------
    # LIVE MEMORY INGESTION
    # -----------------------------

    conversation_text = f"""
USER:
{user_query}

PARTHAGPT:
{ai_response}
"""

    add_memory(
        conversation_text,
        source="live_conversation"
    )

    # -----------------------------
    # RETURN RESPONSE
    # -----------------------------

    return ai_response