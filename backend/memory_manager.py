import os
from datetime import datetime

# -----------------------------
# MEMORY PATH
# -----------------------------

MEMORY_FOLDER = "memory/conversations"

# Create folder if not exists
os.makedirs(MEMORY_FOLDER, exist_ok=True)

# -----------------------------
# SAVE CONVERSATION
# -----------------------------


def save_conversation(user_query, ai_response):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    filename = f"conversation_{timestamp}.txt"

    file_path = os.path.join(
        MEMORY_FOLDER,
        filename
    )

    content = f"""
USER:
{user_query}

PARTHAGPT:
{ai_response}
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path