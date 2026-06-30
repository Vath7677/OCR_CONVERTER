
import sys
import os
import torch
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware


device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"--- SYSTEM STATUS: OCR Engine is initializing on {device.upper()} ---")

# Ensure the 'app' directory is in the system path to resolve imports correctly
app_dir = os.path.dirname(os.path.abspath(__file__))
if app_dir not in sys.path:
    sys.path.append(app_dir)

from ocr_engine.exceptions import OCREngineException
from ocr_engine.pipeline import OCRPipeline

app = FastAPI(title="OCR Converter API")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route implement

# Initialize Pipeline
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
detector_path = os.path.join(base_dir, "model/craft_mlt_25k.pth")
recognizer_path = os.path.join(base_dir, "model/english_g2.pth")

pipeline = OCRPipeline(
    detector_path=detector_path,
    recognizer_path=recognizer_path,
    device=device
)

@app.post("/process-ocr/")
async def process_ocr(file: UploadFile = File(...)):
    try:
        # Read File User Upload
        file_bytes = await file.read()
        
        # call Pipeline for processing
        result = pipeline.execute_ocr(file_bytes)
        
        return result

    except OCREngineException as e:
        # Error exceptions.py
        raise HTTPException(status_code=e.status_code, detail=e.message)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)