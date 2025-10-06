from fastapi import APIRouter as Router, UploadFile, File, HTTPException, Form
import os
import sys
from uuid import uuid4
from pydantic import BaseModel




# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from imageExtraction import extract_text_from_image, get_ocr_health
from ReportGenaration import trade_analysis
from Trading_bot import get_response

router = Router()


class ChatRequest(BaseModel):
    user_input: str





# Directory to save uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def cleanup_old_files():
    """Remove files older than 1 hour to prevent storage bloat"""
    import time
    current_time = time.time()
    for filename in os.listdir(UPLOAD_DIR):
        filepath = os.path.join(UPLOAD_DIR, filename)
        if os.path.isfile(filepath):
            # Remove files older than 1 hour (3600 seconds)
            if current_time - os.path.getctime(filepath) > 3600:
                try:
                    os.remove(filepath)
                except Exception:
                    pass  # Ignore errors during cleanup

@router.get("/router-status")
async def get_router_status():
    return {"status": "OK"}

@router.get("/health")
async def health_check():
    """
    Comprehensive health check including OCR model status
    """
    ocr_health = get_ocr_health()
    return {
        "status": "healthy",
        "ocr_service": ocr_health,
        "upload_dir_exists": os.path.exists(UPLOAD_DIR)
    }



@router.post("/trade-analysis")
async def post_trade_analysis(
    trading_style: str = Form(...),
    trading_strategy: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # Clean up old files
        cleanup_old_files()
        # Validate file type
        allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'}
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"File type {file_extension} not supported. Allowed types: {', '.join(allowed_extensions)}"
            )
        

        # Generate unique filename
        unique_filename = f"{uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        # Check file size (limit to 10MB)
        file_content = await file.read()
        file_size = len(file_content)
        
        if file_size > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=400, detail="File size too large. Maximum size is 10MB")
        
        if file_size == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")

        # Save file to disk
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
        
        # Process the image
        try:
            extracted_texts = extract_text_from_image(file_path)
            if not extracted_texts:
                raise HTTPException(status_code=422, detail="No text could be extracted from the image")

            report = trade_analysis(file_path, extracted_texts, trading_style, trading_strategy)

            response = {
                "message": "Trade analysis successful",
                "report": report,
                
            }
            
            return response
            
        except Exception as processing_error:
     
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=500, 
                detail=f"Error processing image: {str(processing_error)}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    


@router.post("/chat")
async def chat_endpoint(user_input: ChatRequest):
    try:
        response = get_response(user_input.user_input)
        return {"response": response}
    except Exception as e:
        return {"Error": str(e)}