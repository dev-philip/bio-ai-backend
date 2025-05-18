# services/pubmed.py
from Bio import Entrez
from typing import List, Dict
from fastapi.concurrency import run_in_threadpool

# Configure Entrez (required by NCBI)
Entrez.email = "olamideawobusuyi2001@gmail.com"
Entrez.tool = "bio-ai-backend"

def _search_and_extract(claim: str, max_results: int = 100) -> List[Dict[str, str]]:
    handle = Entrez.esearch(db="pubmed", term=claim, retmax=max_results)
    record = Entrez.read(handle)
    ids = record.get("IdList", [])

    if not ids:
        return []

    abstracts = []

    for i in range(0, len(ids), 10):
        batch_ids = ids[i:i + 10]
        fetch_handle = Entrez.efetch(db="pubmed", id=batch_ids, retmode="xml")
        fetch_records = Entrez.read(fetch_handle)

        for article in fetch_records.get('PubmedArticle', []):
            medline = article['MedlineCitation']
            article_data = medline['Article']

            pmid = medline.get('PMID', '')
            title = article_data.get('ArticleTitle', '')

            abstract_section = article_data.get('Abstract', {})
            abstract_text = abstract_section.get('AbstractText', [])
            abstract = " ".join(str(x) for x in abstract_text)

            authors = []
            for author in article_data.get('AuthorList', []):
                last = author.get("LastName", "")
                first = author.get("ForeName", "")
                full = f"{first} {last}".strip()
                if full:
                    authors.append(full)

            journal = article_data.get('Journal', {}).get('Title', '')

            pubdate = (
                article_data.get('Journal', {})
                .get('JournalIssue', {})
                .get('PubDate', {})
                .get('Year', 'Unknown')
            )

            # ✅ Extract DOI from PubmedData
            doi = None
            for id_entry in article.get("PubmedData", {}).get("ArticleIdList", []):
                if id_entry.attributes.get("IdType") == "doi":
                    doi = str(id_entry)

            abstracts.append({
                "pmid": pmid,
                "title": title,
                "abstract": abstract,
                "authors": authors,
                "journal": journal,
                "year": pubdate,
                "doi": doi
            })

    return abstracts

# Async wrapper
async def search_and_extract(claim: str, max_results: int = 100) -> List[Dict[str, str]]:
    return await run_in_threadpool(_search_and_extract, claim, max_results)



# import requests
# from xml.etree import ElementTree


# def search_and_extract(claim):
#     query = f'"{claim.strip()}"'.replace(" ", "+")  # phrase match
#     print("Query:", query)

#     search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
#     params = {
#         "db": "pubmed",
#         "term": query,
#         "retmode": "json",
#         "retmax": 100
#     }

#     response = requests.get(search_url, params=params).json()
#     ids = response["esearchresult"].get("idlist", [])
#     print("PubMed IDs:", ids)

#     if not ids:
#         return []

#     # Fetch abstracts
#     fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
#     abstracts = []
#     for i in range(0, len(ids), 10):
#         batch_ids = ",".join(ids[i:i+10])
#         xml_data = requests.get(fetch_url, params={
#             "db": "pubmed",
#             "id": batch_ids,
#             "retmode": "xml"
#         }).text
#         root = ElementTree.fromstring(xml_data)
#         for article in root.findall(".//PubmedArticle"):
#             title = article.findtext(".//ArticleTitle", "")
#             abstract = article.findtext(".//AbstractText", "")
#             if abstract:  # skip empty ones
#                 abstracts.append({"title": title, "abstract": abstract})
#     return abstracts

# https://pubmed.ncbi.nlm.nih.gov/?term=%22NAD%2B+supplementation+increases+lifespan%22