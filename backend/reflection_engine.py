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

SUMMARY_FOLDER = "memory/summaries"

REFLECTION_FOLDER = "memory/reflections"

os.makedirs(
    REFLECTION_FOLDER,
    exist_ok=True
)

# -----------------------------
# LOAD SUMMARIES
# -----------------------------

def load_summaries():

    summaries = []

    files = os.listdir(
        SUMMARY_FOLDER
    )

    for file in files:

        if file.endswith(".txt"):

            file_path = os.path.join(
                SUMMARY_FOLDER,
                file
            )

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as f:

                summaries.append(
                    f.read()
                )

    return "\n\n".join(
        summaries
    )

# -----------------------------
# GENERATE REFLECTION
# -----------------------------

def generate_reflection():

    summaries_text = load_summaries()

    prompt = f"""
You are an advanced AI reflection engine.

Analyze the following memory summaries and identify:

1. personality patterns
2. recurring interests
3. long-term goals
4. behavioral traits
5. technical growth patterns
6. project preferences
7. motivational patterns
8. future direction

Generate deep reflective insights.

MEMORY SUMMARIES:
{summaries_text}
"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.4
    )

    reflection = response.choices[0].message.content

    return reflection

# -----------------------------
# SAVE REFLECTION
# -----------------------------

def save_reflection(reflection):

    reflection_path = os.path.join(
        REFLECTION_FOLDER,
        "latest_reflection.txt"
    )

    with open(
        reflection_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(reflection)

    print(
        "Reflection saved successfully."
    )

# -----------------------------
# RUN ENGINE
# -----------------------------

if __name__ == "__main__":

    reflection = generate_reflection()

    save_reflection(reflection)

    print("\n===== REFLECTION GENERATED =====\n")

    print(reflection)