# Author: Prof. MM Ghassemi <ghassem3@msu.edu>

import os
import requests

def generate_embedding(text: str):
    """Generate embedding for text using OpenAI API"""
    if not text or not text.strip():
        return [0.0] * 1536
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/embeddings",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "model": "text-embedding-3-small",
                "input": text.strip()
            }
        )
        return response.json()['data'][0]['embedding']
    except:
        return [0.0] * 1536