import os

from backend.memory_summarizer import (
    summarize_conversation
)

# -----------------------------
# PATH
# -----------------------------

CONVERSATION_FOLDER = "memory/conversations"

# -----------------------------
# SUMMARIZE ALL
# -----------------------------

def summarize_all_conversations():

    files = os.listdir(
        CONVERSATION_FOLDER
    )

    for file in files:

        if file.endswith(".txt"):

            file_path = os.path.join(
                CONVERSATION_FOLDER,
                file
            )

            summarize_conversation(
                file_path
            )

# -----------------------------
# RUN
# -----------------------------

if __name__ == "__main__":

    summarize_all_conversations()