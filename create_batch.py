import json
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = "https://api.openai.com/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def upload_file(file_path, purpose="batch"):
    """Upload a file to OpenAI"""
    url = f"{BASE_URL}/files"
    
    with open(file_path, 'rb') as file:
        files = {
            'file': (file_path, file, 'application/jsonl'),
            'purpose': (None, purpose)
        }
        response = requests.post(
            url,
            headers={"Authorization": f"Bearer {API_KEY}"},
            files=files
        )
        
    if response.status_code != 200:
        raise Exception(f"File upload failed: {response.text}")
        
    return response.json()['id']

def create_batch(file_id, endpoint):
    """Create a batch job"""
    url = f"{BASE_URL}/batches"
    
    payload = {
        "input_file_id": file_id,
        "endpoint": endpoint,
        "completion_window": "24h"
    }
    
    response = requests.post(url, headers=HEADERS, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Batch creation failed: {response.text}")
        
    return response.json()

def main():
    if not API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    try:
        # Upload files
        eval_file_id = upload_file('products_data_evaluation.jsonl')
        embed_file_id = upload_file('products_data_embeddings.jsonl')
        
        print(f"Uploaded evaluation file: {eval_file_id}")
        print(f"Uploaded embeddings file: {embed_file_id}")
        
        # Create batch jobs
        eval_batch = create_batch(eval_file_id, "/v1/chat/completions")
        embed_batch = create_batch(embed_file_id, "/v1/embeddings")
        
        print(f"\nCreated evaluation batch job: {eval_batch['id']}")
        print(f"Created embeddings batch job: {embed_batch['id']}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
