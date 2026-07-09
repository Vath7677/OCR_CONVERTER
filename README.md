# OCR Converter 


## Web UI 

*  **[OCR Converter App](https://vath7677.github.io/web_ocr/)**: A high-performance tool built with FastAPI and EasyOCR, featuring a modern web interface for real-time text extraction from images.

### Silde presentation

*  **OCR Slide: Click the link and download it ([https://vath7677.github.io/web_ocr/](https://github.com/Vath7677/OCR_CONVERTER/blob/main/Optical-Character-Recognition.pdf))**

## Features
- **FastAPI Backend**: Clean and fast backend endpoint for OCR processing.
- **EasyOCR Integration**: State-of-the-art OCR engine with multi-language support (English).
- **Vanilla HTML/CSS/JS Frontend**: Clean, modern web UI for image uploading and text results rendering.


## Setup and Python Environment Configuration

This project uses [uv](https://github.com/astral-sh/uv) to manage Python versions, virtual environments, and package dependencies.

### 1. Set Up the Python Environment
Once `uv` is installed, run the following command at the project root to configure the virtual environment and install all project dependencies:
```bash
uv sync
```

### 2. Activate the Environment (Optional)
If you want to manually run python commands directly from your terminal rather than prefixing them with `uv run`:
* **Windows (PowerShell)**:
  ```powershell
  .venv\Scripts\activate
  ```
* **macOS/Linux**:
  ```bash
  source .venv/bin/activate
  ```

### 3. Prerequisite: Model Weights
*Note: Although EasyOCR automatically downloads language weights during the first run directly into the local `model` folder, you can pre-place or add custom model weights at:*
- `model/detector.pt`
- `model/recognizer.pt`


### 4. Alternate option: FastAPI Backend + Static Web Frontend
If you prefer to run the client-server setup:
* **Start the Backend**:
  ```bash
  uv run uvicorn app.main:app --reload
  ```
  *(API: http://localhost:8000)*
  
* **Start the Static Web Server**:
  ```bash
  uv run python -m http.server 3000 --directory frontend
  ```
  *(Frontend: http://localhost:3000)*

## Project Structure Note: Model Weights Location
The `model/` weights folder is located at the project root (outside the `app/` directory) for the following reasons:
1. **Clean Version Control**: Separates large binary weights from source code files, allowing easy Git ignoring via the root `.gitignore`.
2. **Optimized Deployment/Docker builds**: Prevents deployment and container tools from bundling massive local model weights into container images.


