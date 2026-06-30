# OCR Converter App

A high-performance OCR Converter application powered by FastAPI, EasyOCR, and a web-based frontend.

## Features
- **FastAPI Backend**: Clean and fast backend endpoint for OCR processing.
- **EasyOCR Integration**: State-of-the-art OCR engine with multi-language support (English).
- **Vanilla HTML/CSS/JS Frontend**: Clean, modern web UI for image uploading and text results rendering.
- **Streamlit Interactive App**: Rich, modern, single-command app with built-in image uploading, confidence thresholds, detail tables, and result downloading.

## Setup and Python Environment Configuration

This project uses [uv](https://github.com/astral-sh/uv) to manage Python versions, virtual environments, and package dependencies.

### 1. Install `uv` (If not already installed)
* **Windows (PowerShell)**:
  ```powershell
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
* **macOS/Linux**:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### 2. Set Up the Python Environment
Once `uv` is installed, run the following command at the project root to configure the virtual environment and install all project dependencies:
```bash
uv sync
```
This single command automatically:
- Installs the required Python version.
- Creates a local virtual environment under the `.venv/` directory.
- Installs all dependencies (FastAPI, Streamlit, PyTorch, EasyOCR, OpenCV) inside the environment.

### 3. Activate the Environment (Optional)
If you want to manually run python commands directly from your terminal rather than prefixing them with `uv run`:
* **Windows (PowerShell)**:
  ```powershell
  .venv\Scripts\activate
  ```
* **macOS/Linux**:
  ```bash
  source .venv/bin/activate
  ```

### 4. Prerequisite: Model Weights
*Note: Although EasyOCR automatically downloads language weights during the first run directly into the local `model` folder, you can pre-place or add custom model weights at:*
- `model/detector.pt`
- `model/recognizer.pt`

### 2. Run the Streamlit Application (Recommended)
You can run the fully interactive Streamlit application in a single command. It runs the OCR engine directly:
```bash
uv run streamlit run streamlit_app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

### 3. Alternate option: FastAPI Backend + Static Web Frontend
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
3. **Shared Accessibility**: Makes models easily accessible to both the FastAPI backend (`app/main.py`) and the root-level Streamlit dashboard (`streamlit_app.py`).


