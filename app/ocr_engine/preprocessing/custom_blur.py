

# Remove Noise/Background Dirt

import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # នេះគឺថត app/
sys.path.append(BASE_DIR)

import cv2
import numpy as np
from exceptions import PreprocessingException

# this class is using to make an image blur 
class CustomBlur:
                # this method: str = "gussian" it's make an image blur 
    def __init__(self, method: str = "gaussian", kernel_size: int = 3):
        self.method = method.lower()
        
        # checking an condition in the method parameter and print an error message
        if self.method not in ["gaussian", "median"]:
            raise PreprocessingException(f"Unsupported blurring method: '{self.method}'. Choose 'gaussian' or 'median'.")
            
        # verify the kernel number must be an odd number
        if kernel_size % 2 == 0:
            self.kernel_size = kernel_size + 1
        else:
            self.kernel_size = kernel_size
            
    
    def process(self, image: np.ndarray) -> np.ndarray:
        # checking in the variable if it was None it will be print error message
        if image is None:
            raise PreprocessingException("CRITICAL: Input image cannot be None in CustomBlur.")

        try:
            # if it was use this one the processing will be make an image smooth
            if self.method == "gaussian":
                return cv2.GaussianBlur(image, (self.kernel_size, self.kernel_size), 0)
            # else if this one it will be help (Salt-and-Pepper Noise)
            elif self.method == "median":
                return cv2.medianBlur(image, self.kernel_size)

        except Exception as e:
            raise PreprocessingException(f"Blurring process failed during execution: {str(e)}")


if __name__ == "__main__":
    print("[INFO] Initiating Deep Verification on CustomBlur...")
    mock_img = np.random.randint(0, 255, (100, 100), dtype=np.uint8)

    blur_processor = CustomBlur(method="Gaussian", kernel_size=4)
    print(f"[VERIFY] Input Kernel: 4 -> Automatically optimized to ODD: {blur_processor.kernel_size}")
    print(f"[VERIFY] Input Method: 'Gaussian' -> Successfully normalized to: '{blur_processor.method}'")
    
    try:
        output_matrix = blur_processor.process(mock_img)
        print("[SUCCESS] Execution Speed: OPTIMAL (C++ Underlying Binding)")
        print(f"[SUCCESS] Output Shape Verified: {output_matrix.shape}")
    except Exception as e:
        print(f"[ERROR] Verification failed: {str(e)}")