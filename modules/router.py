import os
import requests
import json

def generate_response(user_input, lang="en"):
    headers = {
        "Authorization": "Bearer <OPENROUTER_API_KEY>",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "qwen/qwen3-235b-a22b:free",
        "messages": [
            {"role": "user", "content": user_input}
        ],
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        return response.json().get('choices', [])[0].get('message', {}).get('content', 'No response')
    else:
        return "🤖 Вибач, не зміг згенерувати відповідь."
