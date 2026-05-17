import chromadb

from sentence_transformers import SentenceTransformer

# -----------------------------
# LOAD DATABASE
# -----------------------------

client = chromadb.PersistentClient(
    path="vector_db"
)

collection = client.get_collection(
    name="parthagpt_memory"
)

# -----------------------------
# EMBEDDING MODEL
# -----------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# -----------------------------
# CATEGORY DETECTION
# -----------------------------

def detect_category(query):

    query = query.lower()

    if any(word in query for word in [
        "project",
        "technology",
        "built",
        "system"
    ]):
        return "projects"

    elif any(word in query for word in [
        "goal",
        "career",
        "future",
        "dream"
    ]):
        return "goals"

    elif any(word in query for word in [
        "personality",
        "mindset",
        "strength",
        "weakness",
        "who am i"
    ]):
        return "personality"

    elif any(word in query for word in [
        "linkedin",
        "post",
        "branding"
    ]):
        return "linkedin_posts"

    elif any(word in query for word in [
        "coding",
        "flask",
        "architecture"
    ]):
        return "coding_style"

    elif any(word in query for word in [
        "idea",
        "startup",
        "innovation",
        "hackathon"
    ]):
        return "ideas"

    return None

# -----------------------------
# RETRIEVE MEMORY
# -----------------------------

def retrieve_memory(query, top_k=8):

    category = detect_category(query)

    query_embedding = model.encode(
        query
    ).tolist()

    # -----------------------------
    # SEARCH DATABASE
    # -----------------------------

    if category:

        results = collection.query(

            query_embeddings=[query_embedding],

            n_results=top_k,

            where={"category": category}
        )

    else:

        results = collection.query(

            query_embeddings=[query_embedding],

            n_results=top_k
        )

    documents = results["documents"][0]

    metadatas = results["metadatas"][0]

    # -----------------------------
    # SORT BY IMPORTANCE
    # -----------------------------

    combined = list(
        zip(documents, metadatas)
    )

    combined.sort(

        key=lambda x: x[1].get(
            "importance_score",
            5
        ),

        reverse=True
    )

    # -----------------------------
    # FORMAT RESULTS
    # -----------------------------

    retrieved_chunks = []

    for doc, meta in combined:

        source = meta.get(
            "source",
            "unknown"
        )

        category_name = meta.get(
            "category",
            "general"
        )

        importance = meta.get(
            "importance_score",
            5
        )

        formatted_chunk = f"""
CATEGORY: {category_name}

IMPORTANCE: {importance}

SOURCE: {source}

CONTENT:
{doc}
"""

        retrieved_chunks.append(
            formatted_chunk
        )

    return retrieved_chunks