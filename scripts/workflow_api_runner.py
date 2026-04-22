import json
import urllib.request
import requests

def send_workflow_requests(workflow_json):
    """Send workflow using requests"""
    url = "http://127.0.0.1:8188/prompt"
    payload = {"prompt": workflow_json}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error (requests): {e}")

if __name__ == "__main__":
    # 1. Load your workflow JSON here. This is an empty dummy workflow.
    # In a real scenario, you'd load it from the workflows/ folder.
    dummy_workflow = {}
    
    print("Sending workflow to ComfyUI (http://127.0.0.1:8188)...")
    
    result = send_workflow_requests(dummy_workflow)
    
    if result:
        print("Successfully sent workflow!")
        print(json.dumps(result, indent=2))
