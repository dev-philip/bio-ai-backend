 # Cypher insert/update/query functions
from kg.neo4j_connection import run_query

def insert_claim_graph(data: dict):
        query = """
        MERGE (c:Claim {claim_id: $claim_id})
        SET c.claim = $claim,
            c.cleaned = $cleaned,
            c.semantic_searchable = $semantic_searchable,
            c.source_type = $source_type,
            c.timestamp = $timestamp,
            c.solana_hash = $solana_hash,
            c.verdict = $verdict,
            c.summary = $summary,
            c.reasoning = $reasoning,
            c.null_hypothesis_detected = $null_hypothesis_detected

        // Link biomedical entities
        FOREACH (etype IN keys($biomedical_entities) |
        FOREACH (ename IN $biomedical_entities[etype] |
            MERGE (e:Entity {name: ename, type: etype})
            MERGE (c)-[:MENTIONS]->(e)
        )
        )

        // Link articles
        FOREACH (article IN $semantic_results |
        MERGE (a:Article {pmid: article.pmid})
            SET a.title = article.title,
                a.abstract = article.abstract,
                a.journal = article.journal,
                a.doi = article.doi,
                a.year = article.year,
                a.similarity = article.similarity,
                a.mesh_terms = article.mesh_terms
        MERGE (c)-[:EVIDENCED_BY]->(a)

        // Link authors and affiliations
        FOREACH (i IN range(0, size(article.authors)-1) |
            MERGE (author:Author {name: article.authors[i]})
            MERGE (a)-[:AUTHORED_BY]->(author)
            FOREACH (aff IN [article.affiliations[i]] |
            MERGE (org:Affiliation {name: aff})
            MERGE (author)-[:AFFILIATED_WITH]->(org)
            )
        )
        )
        """ # your cypher
        run_query(query, parameters=data)


# from kg.graph_queries import insert_claim_graph

# @router.post("/claim/to-graph")
# async def push_claim_to_kg(claim: dict):
#     insert_claim_graph(claim)
#     return {"status": "success"}
