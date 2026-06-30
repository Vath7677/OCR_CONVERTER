


import re
from typing import List, Dict, Any


class OCRPostProcessor:
    def __init__(self, confidence_threshold: float = 0.5):
        self.confidence_threshold = confidence_threshold

    def clean_text(self, text: str) -> str:
        cleaned = re.sub(r'[^\w\s\u1780-\u17FF]', '', text) 
        return cleaned.strip()

    def format_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        filtered = [res for res in results if res.get('confidence', 0) >= self.confidence_threshold]
        
        return {
            "status": "success",
            "results": [
                {
                    "text": self.clean_text(res['text']),
                    "confidence": float(res['confidence'])
                } for res in filtered
            ]
        }