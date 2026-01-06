from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from cohere import Client
from cohere.errors import TooManyRequestsError, UnauthorizedError
from uuid import uuid4
import os
import time

# --- 1️⃣ Qdrant client setup ---
QDRANT_URL = "https://35ff8acd-4a88-4c70-a1c2-c58269557efc.europe-west3-0.gcp.cloud.qdrant.io"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.MDYUW19pPMrMuL-QAg9hDyCUozQj6T_cyTD0ppZ1KdE"

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

# --- 2️⃣ Cohere client setup ---
COHERE_API_KEY = "WToZcvC1sAUiZKv9vGWkias6rsxdcTJZZjBf0ffo"
co = Client(COHERE_API_KEY)

COLLECTION_NAME = "book_embeddings"

# --- 3️⃣ Create / recreate collection safely ---
if COLLECTION_NAME not in [c.name for c in client.get_collections().collections]:
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=1024,  # Cohere embed-english-v3.0 size
            distance=Distance.COSINE
        )
    )
    print(f"✅ Collection '{COLLECTION_NAME}' created!")
else:
    print(f"ℹ️ Collection '{COLLECTION_NAME}' already exists, using existing collection.")

# --- 4️⃣ Load book text ---
BOOK_FILE = "book.txt"
if not os.path.exists(BOOK_FILE):
    raise FileNotFoundError(f"Book file '{BOOK_FILE}' not found!")

with open(BOOK_FILE, "r", encoding="utf-8") as f:
    # Split by paragraphs and remove empty lines
    chunks = [chunk.strip() for chunk in f.read().split("\n\n") if chunk.strip()]

if not chunks:
    raise ValueError("Book file is empty or contains no valid text chunks.")

# --- 5️⃣ Embed + upsert in safe batches ---
batch_size = 5   # small batch for free tier
wait_time = 5     # seconds wait between batches
all_embeds = []

for i in range(0, len(chunks), batch_size):
    batch = chunks[i:i+batch_size]
    
    success = False
    while not success:
        try:
            response = co.embed(
                texts=batch,
                model="embed-english-v3.0",
                input_type="search_document"
            )
            success = True
        except TooManyRequestsError:
            print("⚠️ Rate limit hit, waiting 10 seconds...")
            time.sleep(10)
        except UnauthorizedError:
            print("❌ Invalid Cohere API key! Check your key and restart.")
            exit(1)

    all_embeds.extend(response.embeddings)

    # Prepare points for Qdrant
    points = [
        {
            "id": str(uuid4()),
            "vector": response.embeddings[j],
            "payload": {"text": batch[j]}
        }
        for j in range(len(batch))
    ]

    # Upsert points into Qdrant
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"✅ Batch {i//batch_size + 1} upserted ({len(batch)} chunks)")

    # Wait to avoid hitting free tier rate limit
    time.sleep(wait_time)

print(f"✅ {len(chunks)} total chunks embedded successfully into '{COLLECTION_NAME}'")