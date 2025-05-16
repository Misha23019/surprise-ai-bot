import os
import asyncio
from fastapi import FastAPI, Request
from aiogram import types
from dotenv import load_dotenv

from modules.telegram import bot, dp
from modules.scheduler import start_scheduler

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = FastAPI()

@app.post("/")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return {"ok": True}

@app.on_event("startup")
async def on_startup():
    print("Setting webhook...")
    if WEBHOOK_URL:
        await bot.set_webhook(WEBHOOK_URL)
    await start_scheduler()

@app.on_event("shutdown")
async def on_shutdown():
    print("Deleting webhook...")
    await bot.delete_webhook()
