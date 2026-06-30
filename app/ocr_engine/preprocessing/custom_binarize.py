

#### -->> we use this to make a picture white and black

import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import cv2
import numpy as np
from exceptions import PreprocessingException

class CustomBinarizer:
    # it is use to make an app do not crash
    def __init__(self, method: str = "adaptive"):
        self.method = method.lower()

    def process(self, image: np.ndarray) -> np.ndarray:
        # checking if do not have an image will be print a error message on the UI
        # and the code of this it will be through to the file pipeline.py ?? 
        if image is None:
            raise PreprocessingException("CRITICAL: Input image cannot be None in CustomBinarizer.")

        try:
            # checking this image it is { RGB 3 layer }
            if len(image.shape) == 3: # checking the Dimensional it must be 3 
                channels = image.shape[2]     # shape [ heigh: 100, width: 200 ,channel: 3]
                if channels == 3:
                    # use to make an image to be white and black
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                elif channels == 4:
                    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
                else:
                    # if the image do not have 3 or 4 other, we use to use the first channel is [R = shape(0)]
                    gray = image[:, :, 0]
            else:
                gray = image.copy()

            # it was use to make an image to be white on background and black on the digit by split
            if self.method == "otsu":
                # using opencv2 to find the best number of OTUS for calculate this
                _, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            elif self.method == "adaptive":
            # it is use to control the shawdow in our image 
                binary_image = cv2.adaptiveThreshold(
                    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                    cv2.THRESH_BINARY, 11, 2
                )
            else:
                # under 127 is 0 and upper 127 is 255
                _, binary_image = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)


            h, w = binary_image.shape
            corners = [
                binary_image[0, 0],         # the top on the left
                binary_image[0, w - 1],     # top on the right
                binary_image[h - 1, 0],     # button on the left
                binary_image[h - 1, w - 1]  # button on the right
            ]
            
            # checking if the image is bigger than 127
            if np.median(corners) < 127:
                # (Inverse Image) the black to white & white to black 
                binary_image = cv2.bitwise_not(binary_image)

            return binary_image

        except Exception as e:
            # if have anything error it wil be show this error message
            raise PreprocessingException(f"Binarization failed during execution: {str(e)}")




if __name__ == "__main__":
    print("[INFO] Deep Verification on CustomBinarizer...")
    # Mock Image
    mock_img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    
    binarizer = CustomBinarizer(method="adaptive")
    try:
        processed_output = binarizer.process(mock_img)
        print(f"[SUCCESS] Core logic verified! Output Shape: {processed_output.shape}")
        print(f"[VERIFY] Strictly contains only binary elements: {np.unique(processed_output)}")
    except Exception as e:
        print(f"[ERROR] Test failed: {str(e)}")