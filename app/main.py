from fastapi import FastAPI, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.database import Base, engine
#Models - import all models
from app.models import user 
from app.models import student

#Routers
from app.routers import pubmed as pubmed_router
from app.routers import user as user_router
from app.routers import student as student_router
from app.routers import text_extraction as text_extraction_router
from app.routers import text_cleaning as text_cleaning_router
from app.routers import image_analysis as image_analysis_router
from app.routers import neo4j_routes as neo4j_router
from app.routers import claim_result as claim_result_router
from app.routers import solana_routes as solana_router
# End of routers
import logging

# Create all tables
# user.Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI(
    title="FastAPI + MySQL Starter",
    description="A sample FastAPI app with MySQL and modular structure",
    version="1.0.0"
)

# Create the main API router with a shared prefix
api_router = APIRouter(prefix="/api/v1")

# CORS settings (allow all for now; restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic logging config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom error handler
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error occurred on path {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI + MySQL 🚀"}

# Register your sub-routers to the main router
api_router.include_router(user_router.router, prefix="/users", tags=["Users"])
api_router.include_router(student_router.router, prefix="/students", tags=["Students"])
api_router.include_router(text_extraction_router.router, prefix="/nlp", tags=["NLP"])
api_router.include_router(text_cleaning_router.router, prefix="/nlp", tags=["NLP"])
api_router.include_router(image_analysis_router.router, prefix="/vision", tags=["Vision"])
api_router.include_router(pubmed_router.router, prefix="/pubmed", tags=["Pubmed Search"])
api_router.include_router(neo4j_router.router, prefix="/neo4j", tags=["Neo4j Endpoint"])
api_router.include_router(claim_result_router.router, prefix="/claim", tags=["Claims Endpoint"])
api_router.include_router(solana_router.router, prefix="/blockchain", tags=["Blockchain Endpoint"])

# Include the main API router into your FastAPI app
app.include_router(api_router)