from backend.retriever import retrieve_memory

# -----------------------------
# INSPECT MEMORY
# -----------------------------

def inspect_memory(query):

    memories = retrieve_memory(
        query,
        top_k=5
    )

    formatted_memory = "\n\n".join(
        memories
    )

    return f"""
MEMORY INSPECTION RESULTS:

{formatted_memory}
"""