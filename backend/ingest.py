import os
import chromadb

from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

# -----------------------------
# CHROMA DB SETUP
# -----------------------------

client = chromadb.PersistentClient(
    path="vector_db"
)

# -----------------------------
# DELETE OLD COLLECTION
# -----------------------------

try:
    client.delete_collection(
        name="parthagpt_memory"
    )

    print("Old collection deleted.")

except:
    print("No old collection found.")

# -----------------------------
# CREATE NEW COLLECTION
# -----------------------------

collection = client.get_or_create_collection(
    name="parthagpt_memory"
)

# -----------------------------
# EMBEDDING MODEL
# -----------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# -----------------------------
# TEXT SPLITTER
# -----------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

# -----------------------------
# DATA PATH
# -----------------------------

DATA_PATH = "data"

# -----------------------------
# STORAGE
# -----------------------------

documents = []
metadatas = []
ids = []

doc_id = 0

# -----------------------------
# READ FILES
# -----------------------------

for root, dirs, files in os.walk(DATA_PATH):

    for file in files:

        if file.endswith(".txt"):

            file_path = os.path.join(root, file)

            try:

                with open(file_path, "r", encoding="utf-8") as f:

                    content = f.read()

                    # Skip empty files
                    if len(content.strip()) == 0:
                        continue

                    # -----------------------------
                    # DETECT CATEGORY
                    # -----------------------------

                    path_parts = root.split(os.sep)

                    if len(path_parts) > 1:
                        category = path_parts[1]
                    else:
                        category = "general"

                    # -----------------------------
                    # SPLIT INTO CHUNKS
                    # -----------------------------

                    chunks = text_splitter.split_text(
                        content
                    )

                    # -----------------------------
                    # STORE CHUNKS
                    # -----------------------------

                    for chunk in chunks:

                        documents.append(chunk)

                        metadatas.append({
                            "source": file_path,
                            "file_name": file,
                            "category": category
                        })

                        ids.append(str(doc_id))

                        doc_id += 1

                    print(f"Processed: {file}")

            except Exception as e:

                print(f"Error reading {file}: {e}")

# -----------------------------
# CREATE EMBEDDINGS
# -----------------------------

print("\nCreating embeddings...")

embeddings = model.encode(
    documents,
    show_progress_bar=True
).tolist()

# -----------------------------
# STORE IN CHROMADB
# -----------------------------

collection.add(
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas,
    ids=ids
)

# -----------------------------
# FINAL OUTPUT
# -----------------------------

print("\n===================================")
print("ParthaGPT Memory Ingestion Complete")
print("===================================")

print(f"Total Chunks Stored: {len(documents)}")
print(f"Total Metadata Entries: {len(metadatas)}")
print(f"Database Location: vector_db/")
print("Chunking + Categorization Successful")