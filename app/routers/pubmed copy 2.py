from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.pubmed import search_and_extract

router = APIRouter()

class ClaimRequest(BaseModel):
    claim: str

# @router.post("/pubmed/search")
# def search_pubmed(request: ClaimRequest):
#     try:
#         results = search_and_extract(request.claim)
#         return {"results": results}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@router.post("/pubmed/search")
async def search_pubmed(request: ClaimRequest):
    try:
        results = await search_and_extract(request.claim)  # ✅ await here
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
