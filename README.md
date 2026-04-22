# ComfyUI Multimodal Pipeline

This project is a setup for running ComfyUI multimodal pipelines via API.

## Directory Structure
- `workflows/`: Store ComfyUI workflow JSON files here.
- `scripts/`: Python scripts to interact with ComfyUI API.
- `assets/`: Images, videos, and other assets for the workflows.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run ComfyUI server locally (default: `http://127.0.0.1:8188`).
3. Run the API runner script:
   ```bash
   python scripts/workflow_api_runner.py
   ```
