import json
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv('OPENAI_API_KEY')
BASE_URL = "https://api.openai.com/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_batch_status(batch_id):
    """Get the status of a batch job"""
    url = f"{BASE_URL}/batches/{batch_id}"
    
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        raise Exception(f"Failed to get batch status: {response.text}")
        
    return response.json()

def main():
    if not API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    try:
        eval_status = get_batch_status("batch_678c6b2950088190af53d5e392583a21")
        embed_status = get_batch_status("batch_678c6b2a4dd4819094c48dd1cc3ac6d1")
        
        print(f"\nEvaluation batch status: {eval_status['status']}")
        print(f"Embeddings batch status: {embed_status['status']}")
        # Check if both batches are completed
        if eval_status['status'] == 'completed' and embed_status['status'] == 'completed':
            # Get output file IDs
            eval_file_id = eval_status['output_file_id'] 
            embed_file_id = embed_status['output_file_id']
            
            # Get file contents
            eval_url = f"{BASE_URL}/files/{eval_file_id}/content"
            embed_url = f"{BASE_URL}/files/{embed_file_id}/content"
            
            eval_response = requests.get(eval_url, headers=HEADERS)
            embed_response = requests.get(embed_url, headers=HEADERS)
            
            if eval_response.status_code != 200:
                raise Exception(f"Failed to get evaluation results: {eval_response.text}")
            if embed_response.status_code != 200:
                raise Exception(f"Failed to get embedding results: {embed_response.text}")
                
            # Save results to files
            with open('evaluation_results.jsonl', 'w') as f:
                f.write(eval_response.text)
            with open('embedding_results.jsonl', 'w') as f:
                f.write(embed_response.text)
                
            print("\nResults downloaded and saved to:")
            print("- evaluation_results.jsonl")
            print("- embedding_results.jsonl")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
