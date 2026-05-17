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
# MEMORY SCORING
# -----------------------------

def calculate_importance(text):

    text = text.lower()

    score = 5

    # High importance keywords

    important_keywords = [
        "goal",
        "dream",
        "career",
        "ai",
        "project",
        "startup",
        "future",
        "personality",
        "ambition",
        "vision",
        "agent",
        "learning",
        "memory"
    ]

    # Low importance keywords

    low_keywords = [
        "hello",
        "hi",
        "okay",
        "thanks",
        "cool"
    ]

    # Increase score

    for word in important_keywords:

        if word in text:
            score += 1

    # Decrease score

    for word in low_keywords:

        if word in text:
            score -= 1

    # Clamp score

    score = max(1, min(score, 10))

    return score

# -----------------------------
# ADD MEMORY
# -----------------------------

def add_memory(text, source="conversation"):

    importance_score = calculate_importance(
        text
    )

    embedding = model.encode(
        text
    ).tolist()

    memory_id = f"live_{hash(text)}"

    collection.add(

        documents=[text],

        embeddings=[embedding],

        metadatas=[{
            "source": source,
            "category": "conversation_memory",
            "importance_score": importance_score
        }],

        ids=[memory_id]
    )

    print(
        f"Memory Added | Importance: {importance_score}"
    )