from backend.tools.file_writer import (
    write_file
)

# -----------------------------
# GENERATE REPORT
# -----------------------------

def generate_report(title, content):

    file_name = title.lower().replace(
        " ",
        "_"
    )

    file_path = f"generated_reports/{file_name}.txt"

    result = write_file(
        file_path,
        content
    )

    return result