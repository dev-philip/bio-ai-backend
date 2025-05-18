from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.database import engine
from app.models import user
#Routers
from app.routers import pubmed as pubmed_router
from app.routers import user as user_router
from app.routers import text_extraction as text_extraction_router
from app.routers import text_cleaning as text_cleaning_router
from app.routers import image_analysis as image_analysis_router
# End of routers
import logging

# Create all tables
user.Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI(
    title="FastAPI + MySQL Starter",
    description="A sample FastAPI app with MySQL and modular structure",
    version="1.0.0"
)

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

# Register user routes
app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(text_extraction_router.router, prefix="/nlp", tags=["NLP"])  
app.include_router(text_cleaning_router.router, prefix="/nlp", tags=["NLP"])
app.include_router(image_analysis_router.router, prefix="/vision", tags=["Vision"])
app.include_router(pubmed_router.router, prefix="/api", tags=["Pubmed Search"])

