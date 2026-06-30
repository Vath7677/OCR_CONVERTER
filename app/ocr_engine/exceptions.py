## this was use to tell us and protect the code which place have error

# this will be see an error message from here when an API is error
class OCREngineException(Exception):
    def __init__(self, message: str, status_code: int = 402):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

    def __str__(self):
        return f"[{self.status_code}] {self.message}"
    
# this will be show an error message when the Preprocessing error
class PreprocessingException(OCREngineException):
    def __init__(self, message: str = "Error during image preprocessing."):
        super().__init__(message, status_code=400)

# it will be show a message when the detection/ border box was error
class DetectionException(OCREngineException):
    def __init__(self, message: str = "Error during object/text detection stage."):
        super().__init__(message, status_code=501)


# it is an recognition or we call prediction
class RecognitionException(OCREngineException):
    def __init__(self, message: str = "Text recognition failed."):
        super().__init__(message, status_code=500)

# this will be show an error message when the Postprocessing/Cropping error
class PostprocessingException(OCREngineException):
    def __init__(self, message: str = "Error during post-detection image processing stage."):
        super().__init__(message, status_code=423)

# it was be an error input 
class InvalidInputException(OCREngineException):
    def __init__(self, message: str = "Invalid input file format."):
        super().__init__(message, status_code=422)