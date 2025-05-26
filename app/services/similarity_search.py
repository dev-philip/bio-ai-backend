from sentence_transformers import SentenceTransformer, util
import torch

# Load embedding model (you can move this to global scope in your router)
model = SentenceTransformer('all-MiniLM-L6-v2')

def rank_articles_by_similarity(claim: str, articles: list, top_k: int = 5):
    # Step 1: Embed the claim
    claim_embedding = model.encode(claim, convert_to_tensor=True)

    # Step 2: Embed semantic strings from articles
    semantic_texts = [article["semantic_string"] for article in articles]
    article_embeddings = model.encode(semantic_texts, convert_to_tensor=True)

    # Step 3: Compute cosine similarity
    similarities = util.cos_sim(claim_embedding, article_embeddings)[0]  # 1D tensor

    # Step 4: Rank by similarity
    sorted_indices = torch.argsort(similarities, descending=True)

    # Step 5: Return top-k results with similarity score
    ranked_results = []
    for idx in sorted_indices[:top_k]:
        article = articles[idx]
        ranked_results.append({
            "title": article["title"],
            "abstract": article["abstract"],
            # "mesh_terms": article["mesh_terms"],
            "semantic_string": article["semantic_string"],
            "similarity": round(float(similarities[idx]), 4)
        })

    return ranked_results
