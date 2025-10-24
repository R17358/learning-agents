import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

SERP_API = os.getenv('SERP_API')

def serp_search(query:str)->str:
    try:
        url = "https://www.searchapi.io/api/v1/search"
        params = {
        "engine": "google",
        "q": query,
        "api_key": SERP_API
        }

        response = requests.get(url, params=params)
        
        return response.json()
    except Exception as e:
        print(e)
        return {}

query = input('Enter query: ')
out = serp_search(query)

print(json.dumps(out, indent=2, ensure_ascii=False))