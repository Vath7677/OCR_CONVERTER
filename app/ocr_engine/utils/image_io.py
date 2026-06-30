

import cv2
import numpy as np

def decode_image_from_bytes(file_bytes: bytes) -> np.ndarray:
    if not file_bytes:
        raise ValueError("Cannot decode image because the uploaded file bytes are empty.")
        
    nparr = np.frombuffer(file_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if image is None:
        raise ValueError("Failed to decode image. The file may be corrupted or in an unsupported format.")

    return image

def encode_image_to_bytes(image: np.ndarray, format_ext: str = '.jpg') -> bytes:
    if image is None:
        raise ValueError("Cannot encode image because the provided image data is None.")
        
    success, encoded_img = cv2.imencode(format_ext, image)
    if not success:
        raise IOError(f"Failed to encode the image into {format_ext} format.")
        
    return encoded_img.tobytes()





'''
def load_image(file_path: str) -> np.ndarray:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No image file found at: {file_path}")
        
    try:
        file_bytes = np.fromfile(file_path, dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    except Exception as e:
        raise ValueError(f"Failed to read image data: {str(e)}")

    if image is None:
        raise ValueError(f"Image file is corrupted or invalid: {file_path}")
        
    return image        '''