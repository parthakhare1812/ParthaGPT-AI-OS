import os

# -----------------------------
# WRITE FILE
# -----------------------------

def write_file(file_path, content):

    try:

        os.makedirs(
            os.path.dirname(file_path),
            exist_ok=True
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(content)

        return f"File saved successfully: {file_path}"

    except Exception as e:

        return f"Error writing file: {e}"