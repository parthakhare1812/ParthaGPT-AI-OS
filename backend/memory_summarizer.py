import os

from groq import Groq

from dotenv import load_dotenv

# -----------------------------
# LOAD ENV
# -----------------------------

load_dotenv()

# -----------------------------
# GROQ CLIENT
# -----------------------------

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# -----------------------------
# PATHS
# -----------------------------

CONVERSATION_FOLDER = "memory/conversations"

SUMMARY_FOLDER = "memory/summaries"

os.makedirs(
    SUMMARY_FOLDER,
    exist_ok=True
)

# -----------------------------
# SUMMARIZE MEMORY
# -----------------------------

def summarize_conversation(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        conversation = f.read()

    # -----------------------------
    # PROMPT
    # -----------------------------

    prompt = f"""
You are an AI memory compression system.

Summarize the following conversation into:
- key ideas
- important goals
- personality insights
- preferences
- technical interests
- important long-term information

Keep only meaningful long-term memory.

CONVERSATION:
{conversation}
"""

    # -----------------------------
    # GENERATE SUMMARY
    # -----------------------------

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.3
    )

    summary = response.choices[0].message.content

    # -----------------------------
    # SAVE SUMMARY
    # -----------------------------

    file_name = os.path.basename(
        file_path
    )

    summary_file = os.path.join(
        SUMMARY_FOLDER,
        f"summary_{file_name}"
    )

    with open(
        summary_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(summary)

    print(
        f"Summary created: {summary_file}"
    )

    return summary