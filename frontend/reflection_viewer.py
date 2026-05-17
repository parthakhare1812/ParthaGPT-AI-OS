import os

# -----------------------------
# LOAD REFLECTIONS
# -----------------------------

def load_reflections():

    reflection_folder = "memory/reflections"

    reflections = []

    if not os.path.exists(reflection_folder):
        return reflections

    files = os.listdir(reflection_folder)

    for file in files:

        if file.endswith(".txt"):

            file_path = os.path.join(
                reflection_folder,
                file
            )

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as f:

                content = f.read()

                reflections.append({
                    "file": file,
                    "content": content
                })

    return reflections