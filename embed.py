import json
import faiss
import pickle
from sentence_transformers import SentenceTransformer


with open("data/shl_catalog.json", "r", encoding="utf-8") as f:
    assessments = json.load(f)


model = SentenceTransformer("all-MiniLM-L6-v2")

texts = []
metadata = []

for item in assessments:
    text = f"""
    Name: {item.get("name", "")}
    Description: {item.get("description", "")}
    Job Levels: {", ".join(item.get("job_levels", []))}
    Keys: {", ".join(item.get("keys", []))}
    """

    texts.append(text)
    metadata.append(item)

embeddings = model.encode(texts)

dimension = len(embeddings[0])
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, "faiss_index/index.faiss")

with open("faiss_index/metadata.pkl", "wb") as f:
    pickle.dump(metadata, f)

print(f"Embedded {len(metadata)} assessments successfully.")