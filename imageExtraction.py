# Initialize PaddleOCR instance with singleton pattern for performance
from paddleocr import PaddleOCR
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OCRService:
    """
    Singleton OCR service to ensure PaddleOCR model is loaded only once
    This prevents the 30-60 second model loading delay on every request
    """
    _instance = None
    _ocr = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                # Double-check locking pattern
                if cls._instance is None:
                    cls._instance = super(OCRService, cls).__new__(cls)
        return cls._instance
    
    def get_ocr(self):
        """
        Lazy loading of OCR model - only loads when first needed
        """
        if self._ocr is None:
            with self._lock:
                if self._ocr is None:
                    logger.info("Loading PaddleOCR model (this may take 30-60 seconds on first use)...")
                    self._ocr = PaddleOCR(
                        use_doc_orientation_classify=False,
                        use_doc_unwarping=False,
                        use_textline_orientation=False
                    )
                    logger.info("PaddleOCR model loaded successfully!")
        return self._ocr

# Global OCR service instance
ocr_service = OCRService()

def warm_up_ocr():
    """
    Warm up the OCR model by pre-loading it
    Call this function during application startup to avoid first-request delay
    """
    logger.info("Warming up OCR model...")
    ocr_service.get_ocr()
    logger.info("OCR model warm-up completed!")

def get_ocr_health():
    """
    Check if OCR model is loaded and ready
    Returns:
        dict: Health status of OCR service
    """
    try:
        is_loaded = ocr_service._ocr is not None
        return {
            "status": "healthy" if is_loaded else "not_loaded",
            "model_loaded": is_loaded
        }
    except Exception as e:
        return {
            "status": "error",
            "model_loaded": False,
            "error": str(e)
        }

def extract_text_from_image(image_path):
    """
    Extract text from image using singleton OCR service
    Args:
        image_path (str): Path to the image file
    Returns:
        list: Extracted text strings from the image
    """
    try:
        logger.info(f"Starting OCR extraction for: {image_path}")
        
        # Get OCR instance (lazy loaded on first call)
        ocr = ocr_service.get_ocr()
        
        # Run OCR inference on the provided image path
        result = ocr.predict(input=image_path)
        
        logger.info("OCR inference completed successfully")
        
    except Exception as e:
        logger.error(f"Error during OCR inference: {str(e)}")
        raise

    extracted_texts = []

    # Extract only the rec_texts from the result
    for res in result:
        rec_texts = res.get('rec_texts', [])
        extracted_texts.extend(rec_texts)
        logger.info(f"Extracted {len(rec_texts)} text elements from image")
        
        # Optional: Save results to output directory (disabled by default for performance)
        # Uncomment these lines if you need to save visualization files
        # res.save_to_img("output")
        # res.save_to_json("output")

    logger.info(f"Total extracted texts: {len(extracted_texts)}")
    return extracted_texts





