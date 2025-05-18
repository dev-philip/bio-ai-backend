import requests

BASE_URL = "https://api.semanticscholar.org/graph/v1"

def get_citations_and_references(doi: str):
    if not doi:
        return {"citations": [], "references": []}
    
    url = f"{BASE_URL}/paper/DOI:{doi}"
    params = {
        "fields": "title,citations.title,citations.authors,references.title,references.authors"
    }

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return {"citations": [], "references": []}
        data = response.json()

        citations = [
            {
                "title": item.get("title"),
                "authors": [a.get("name") for a in item.get("authors", [])]
            }
            for item in data.get("citations", [])
        ]

        references = [
            {
                "title": item.get("title"),
                "authors": [a.get("name") for a in item.get("authors", [])]
            }
            for item in data.get("references", [])
        ]

        return {
            "citations": citations,
            "references": references
        }

    except Exception as e:
        print("Semantic Scholar error:", e)
        return {"citations": [], "references": []}


# What to Improve open

# For rate limiting, Semantic Scholar allows 100 requests per 5 minutes. 
# Cache the citations/references to avoid repeated calls