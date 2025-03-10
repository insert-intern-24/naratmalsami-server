import httpx
from app.config import settings
from app.schemas.ai import DifyInput
import json
import re

DIFY_URL = settings.dify_url
DIFY_KEY = settings.dify_key

async def dify(data: DifyInput):
    foreign_words = ','.join(word for word in data['origin_word'])
    sentence = data['sentence']
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DIFY_URL}/workflows/run",
            headers={
                "Authorization": f"Bearer {DIFY_KEY}",
            },
            json={
                "inputs": {
                    "foreign_words": foreign_words,
                    "text_to_replace": sentence,
                },
                "response_mode": "blocking",
                "user": "asdfasdf-123"
            },
            timeout=30
        )
        
    if response.status_code != 200:
        raise Exception(f"Error")
    
    response = response.json()
    matches = re.findall(r'\{(.*?)\}', response['data']['outputs']['text'], re.DOTALL)
    
    json_data = json.loads('{' + (matches[0] if matches else '{}') + '}')

    return json_data
    