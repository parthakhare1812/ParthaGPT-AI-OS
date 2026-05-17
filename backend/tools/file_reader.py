import os

# -----------------------------
# READ FILE
# -----------------------------

def read_file(file_path):

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            content = f.read()

        return content

    except Exception as e:

        return f"Error reading file: {e}"