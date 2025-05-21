# start.py
import os
import asyncio
from app import app, start_bot
import uvicorn

async def main():
    config = uvicorn.Config(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)), log_level="info")
    server = uvicorn.Server(config)

    bot_task = asyncio.create_task(start_bot())
    server_task = asyncio.create_task(server.serve())

    await asyncio.gather(bot_task, server_task)

if __name__ == "__main__":
    asyncio.run(main())
