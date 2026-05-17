import os

# -----------------------------
# LOAD MEMORY FILES
# -----------------------------

def load_memories():

    memory_folder = "memory/conversations"

    memories = []

    if not os.path.exists(memory_folder):
        return memories

    files = os.listdir(memory_folder)

    for file in files:

        if file.endswith(".txt"):

            file_path = os.path.join(
                memory_folder,
                file
            )

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as f:

                content = f.read()

                memories.append({
                    "file": file,
                    "content": content
                })

    return memories