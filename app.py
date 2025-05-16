import asyncio
from modules.telegram import start_bot
from modules.scheduler import start_scheduler

async def main():
    await start_bot()
    await start_scheduler()

if __name__ == "__main__":
    asyncio.run(main())
