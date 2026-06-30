

# this was be use for (Rotate an image) or (Deskew / Perspective Transform)

import sys
import os
import cv2
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from exceptions import PreprocessingException

class CustomTransform:

    def __init__(self, method="auto_deskew"): 
        self.method = method
        
        # checking an condtion Input Parameter
        if self.method not in ["auto_deskew", "none"]:
            raise PreprocessingException(
                f"Unsupported transformation method: '{self.method}'. "
                f"Choose 'auto_deskew' or 'none'."
            )

    def _determine_skew_angle(self, image: np.ndarray) -> float:
        if len(image.shape) == 3:
            # convert it to gray color
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # convert the image to black and white 
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # checking the coordinate by np.where and the column_stack to collect the info
        coords = np.column_stack(np.where(thresh > 0))
        
        # using to find an angle
        angle = cv2.minAreaRect(coords)[2]

        # using to finding the angle coordination
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
            
        return angle

    def process(self, image: np.ndarray) -> np.ndarray:
        # checking for the None
        if image is None:
            raise PreprocessingException("CRITICAL: Input image cannot be None in CustomTransform.")

        try:
            # if the parameter is none it will return back an image 
            if self.method == "none":
                return image

            # the angle have checking before use to calcalate in the [._determine_skew_angle]
            if self.method == "auto_deskew":
                angle = self._determine_skew_angle(image)
                
                if abs(angle) < 0.5:
                    return image

                # taking only index (0,1). but .shape[height, width, channel]
                (h, w) = image.shape[:2]
                # calculate just want to get interger number 
                center = (w // 2, h // 2)
                
                # this will be make an transform
                M = cv2.getRotationMatrix2D(center, angle, 1.0)
                
                rotated = cv2.warpAffine(
                    image, M, (w, h), 
                    flags=cv2.INTER_CUBIC, 
                    borderMode=cv2.BORDER_CONSTANT, 
                    borderValue=(255, 255, 255)
                )
                return rotated

        except Exception as e:
            raise PreprocessingException(f"Transformation process failed during execution: {str(e)}")
