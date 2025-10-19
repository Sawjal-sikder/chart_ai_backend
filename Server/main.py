from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routes import router
import os
import sys
import logging

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ChartAI Trading Analysis API", version="1.0.0", swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}})

@app.on_event("startup")
async def startup_event():
    """
    Startup event to warm up OCR model
    This prevents the first request from taking 30-60 seconds
    """
    try:
        from imageExtraction import warm_up_ocr
        logger.info("Starting OCR model warm-up...")
        warm_up_ocr()
        logger.info("Application startup completed successfully!")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        # Don't fail startup, just log the error

# Mount static files directory for serving uploaded images
uploads_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}



app.include_router(router, prefix="/api/v1")