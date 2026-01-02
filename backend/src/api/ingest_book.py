from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from cohere import Client
from uuid import uuid4

client = QdrantClient(
    url="https://1e2951c0-86cd-480e-9cca-b040c24f65e6.europe-west3-0.gcp.cloud.qdrant.io:6333",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.ppIAgtT0Fo6dN40_a8dpTnb6I7_qGRj6_tBs0zZts5M"
)

co = Client("hQjHRK5mE09ZcE2SkBZuXO6R1EzgjDZ4W1uoxG1a")

COLLECTION_NAME = "book_embeddings"

# 1️⃣ create collection
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=1024,
        distance=Distance.COSINE
    )
)

# 2️⃣ load book text (example)
with open("book.txt", "r", encoding="utf-8") as f:
    chunks = f.read().split("\n\n")

# 3️⃣ embed + insert
embeds = co.embed(
    texts=chunks,
    model="embed-english-v3.0"
).embeddings

points = [
    {
        "id": str(uuid4()),
        "vector": embeds[i],
        "payload": {"text": chunks[i]}
    }
    for i in range(len(chunks))
]

client.upsert(collection_name=COLLECTION_NAME, points=points)

print("✅ Book embedded successfully")
