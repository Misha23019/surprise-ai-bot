#modules/gpt_api.py
import os
import logging
import httpx
from modules.limits import increase

logging.basicConfig(level=logging.INFO)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = "qwen/qwen3-235b-a22b:free"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

if OPENROUTER_API_KEY:
    logging.info(f"✅ Using API key: {OPENROUTER_API_KEY[:5]}...")
else:
    logging.error("❌ OPENROUTER_API_KEY is not set!")
    raise ValueError("OPENROUTER_API_KEY is not set!")

async def ask_gpt(user_id: str, messages: list[dict]) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(OPENROUTER_API_URL, headers=headers, json=data)
            response.raise_for_status()

            result = response.json()
            content = result["choices"][0]["message"]["content"].strip()

            # Лимит учитывается только при успешной генерации
            await increase(user_id)

            return content

    except httpx.HTTPStatusError as http_err:
        logging.error(f"❌ HTTP error from GPT: {http_err.response.status_code} - {http_err.response.text}")
    except httpx.RequestError as req_err:
        logging.error(f"❌ Request error when contacting GPT: {req_err}")
    except Exception as e:
        logging.error(f"❌ Unexpected error from GPT: {type(e).__name__}: {e}")

    return "⚠️ Виникла помилка при зверненні до GPT. Спробуйте ще раз пізніше."
