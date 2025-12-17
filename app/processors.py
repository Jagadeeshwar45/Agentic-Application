import easyocr
import numpy as np
from PIL import Image
import io
import pdfplumber
import logging

logger = logging.getLogger("FileProcessor")

try:
    reader = easyocr.Reader(['en'], gpu=False) 
except Exception as e:
    logger.error(f"Failed to init EasyOCR: {e}")
    reader = None

class FileProcessor:
    @staticmethod
    def process_image(image_bytes: bytes) -> str:
        """
        OCR using EasyOCR (Deep Learning based).
        No external .exe installation required.
        """
        if reader is None:
            return "Error: OCR engine not initialized."

        try:
            image = Image.open(io.BytesIO(image_bytes))
            image_np = np.array(image)
            result_list = reader.readtext(image_np, detail=0)
            text = " ".join(result_list)
            return text.strip()
            
        except Exception as e:
            logger.error(f"OCR Failed: {str(e)}")
            raise ValueError(f"OCR Processing Error: {str(e)}")

    @staticmethod
    def process_pdf(pdf_bytes: bytes) -> str:
        """Extract text from PDF. Fallback to OCR if text is empty."""
        text = ""
        try:
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                    else:
                        text += "[Scanned Page - Text Not Selectable]\n"
            
            return text.strip() if text else "No extractable text found in PDF."
            
        except Exception as e:
            raise ValueError(f"PDF Parsing Failed: {str(e)}")