from fastapi import APIRouter
from app.kg.neo4j_connection import driver  # or run_query if you're using wrapper

router = APIRouter()

@router.get("/test")
def test_neo4j_connection():
    try:
        with driver.session() as session:
            result = session.run("RETURN 'Neo4j connection works!' AS message")
            message = result.single()["message"]
        return {"status": "success", "message": message}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
