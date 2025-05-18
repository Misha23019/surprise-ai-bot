import os
import json
import logging
import httpx

logging.basicConfig(level=logging.INFO)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if OPENROUTER_API_KEY:
    logging.info(f"Using API key: {OPENROUTER_API_KEY[:5]}...")
else:
    logging.error("OPENROUTER_API_KEY is not set!")
    raise ValueError("OPENROUTER_API_KEY is not set!")

async def ask_gpt(messages):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "qwen/qwen3-235b-a22b:free",
        "messages": messages,
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]

    except httpx.HTTPStatusError as http_err:
        logging.error(f"❌ HTTP error from GPT: {http_err.response.status_code} - {http_err.response.text}")
    except httpx.RequestError as req_err:
        logging.error(f"❌ Request error when contacting GPT: {req_err}")
    except Exception as e:
        logging.error(f"❌ Unexpected error from GPT: {e}")

    return "⚠️ Виникла помилка при зверненні до GPT."
