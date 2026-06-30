

import os
from .exceptions import (
    OCREngineException,
    PreprocessingException,
    DetectionException,
    PostprocessingException,  
    RecognitionException
)


from .utils.image_io import decode_image_from_bytes
from .utils.postprocessing import OCRPostProcessor
from .preprocessing.custom_binarize import CustomBinarizer
from .preprocessing.custom_blur import CustomBlur
from .preprocessing.custom_transform import CustomTransform


class OCRPipeline:
    def __init__(self, detector_path: str, recognizer_path: str, languages: list = None, device="cpu"):

        self.detector_path = detector_path
        self.recognizer_path = recognizer_path
        self.languages = languages if languages is not None else ['en']
        
        # Initialize Preprocessors
        self.binarizer = CustomBinarizer(method="adaptive")
        self.blurrer = CustomBlur(method="gaussian", kernel_size=3)
        self.transformer = CustomTransform(method="auto_deskew")
        self.post_processor = OCRPostProcessor()
        
        # EasyOCR Reader
        import torch
        import easyocr
        
        # Determine model storage directory (parent of detector_path)
        model_storage_dir = os.path.dirname(detector_path) if detector_path else None
        if model_storage_dir:
            os.makedirs(model_storage_dir, exist_ok=True)
            
        print(f"[INFO] Initializing EasyOCR Reader for {self.languages} in {model_storage_dir}...")

        gpu_enabled = torch.cuda.is_available() or torch.backends.mps.is_available()
        print(f"[INFO] Initializing EasyOCR Reader for {self.languages} in {model_storage_dir}...")

        try:
            self.reader = easyocr.Reader(
                self.languages, 
                gpu=gpu_enabled,
                model_storage_directory=model_storage_dir,
                download_enabled=False
            )
            print(f"[INFO] EasyOCR Reader initialized (GPU={gpu_enabled}).")
        except Exception as e:
            raise OCREngineException(f"Failed to initialize EasyOCR Reader: {str(e)}")

    def run_preprocessing(self, file_bytes: bytes):
        print("[INFO] Stage 1: Starting Preprocessing...")
        try:
            image = decode_image_from_bytes(file_bytes)
            # Chain processing: transform (deskew) -> return for EasyOCR
            # We skip heavy binarization/blurring by default because CRAFT detector (in EasyOCR)
            # works best on color or original contrast levels.
            image = self.transformer.process(image)
            return image
        except Exception as e:
            raise PreprocessingException(f"Failed during Preprocessing Stage: {str(e)}")

    def run_detection(self, preprocessed_image):
        # Deprecated: EasyOCR performs detection & recognition in one pass
        pass

    def run_postprocessing(self, ocr_results):
        # Custom cleaning and post-processing if needed
        try:
            cleaned_results = []
            for res in ocr_results:
                cleaned_text = self.post_processor.clean_text(res['text'])
                if cleaned_text:
                    cleaned_results.append({
                        "box": res['box'],
                        "text": cleaned_text,
                        "confidence": res['confidence']
                    })
            return cleaned_results
        except Exception as e:
            raise PostprocessingException(f"Failed during Postprocessing Stage: {str(e)}")

    def execute_ocr(self, file_bytes: bytes) -> dict:
        print("[START] Processing OCR Pipeline...")
        
        processed_img = self.run_preprocessing(file_bytes)
        
        try:
            # Run EasyOCR
            results = self.reader.readtext(processed_img)
            
            # Format results
            ocr_results = []
            for bbox, text, confidence in results:
                # Convert coords to list of ints
                formatted_bbox = [[int(pt[0]), int(pt[1])] for pt in bbox]
                ocr_results.append({
                    "box": formatted_bbox,
                    "text": text,
                    "confidence": float(confidence)
                })
            
            # Run optional post-processing cleanup
            final_results = self.run_postprocessing(ocr_results)
            
            # Get dimensions
            h, w = processed_img.shape[:2]
            
            print("[SUCCESS] OCR Pipeline completed successfully!")
            return {
                "status": "success",
                "width": w,
                "height": h,
                "results": final_results
            }
            
        except Exception as e:
            print(f"[ERROR] OCR Pipeline execution failed: {str(e)}")
            raise OCREngineException(f"Failed during text recognition stage: {str(e)}")