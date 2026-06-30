import os
import torch

class OCREngineConfig:

    ###  this is use for make a path for AI make sure that AI is on the right path and must be use a Cuda
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    
    # point to folder model
    MODEL_DIR = os.path.join(BASE_DIR, "model")
    
    # define a path
    DETECTOR_PATH = os.path.join(MODEL_DIR, "craft_mlt_25k.pth")
    RECOGNIZER_PATH = os.path.join(MODEL_DIR, "english_g2.pth")
    
    if torch.cuda.is_available():
        DEVICE = torch.device("cuda")
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        DEVICE = torch.device("mps")
    else:
        DEVICE = torch.device("cpu")

    # use to detection digit 
    DETECTION_CONF_THRESHOLD = 0.25  
    CRNN_IMAGE_SIZE = (100, 32)      
    
    VOCABULARY = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .,/-"

config = OCREngineConfig()