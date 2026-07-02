import faiss
import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("faiss_index/index.faiss")
with open("faiss_index/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)


def search_assessments(query, top_k=5):
   
    query_embedding = model.encode([query])

    
    distances, indices = index.search(query_embedding, top_k)

    results = []

    for idx in indices[0]:
        results.append(metadata[idx])

    return results


if __name__ == "__main__":
    query = "Java developer with leadership skills"
    results = search_assessments(query)

    print("\nTop Matches:\n")

    for r in results:
        print("Name:", r["name"])
        print("Description:", r["description"][:150])
        print("URL:", r["link"])
        print("-" * 50)