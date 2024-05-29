import asyncio
from dispatcher import dp
from bot import bot
from functions import *


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
