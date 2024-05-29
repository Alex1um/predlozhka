"""
Start bot
"""
import asyncio
from dispatcher import dp
from bot import bot
from functions import *


async def main():
    """
    Asynchronous function that starts the polling process for the bot.

    This function is responsible for starting the polling process for the bot. It uses the `dp` object to start polling for updates from the bot.

    Parameters:
        None

    Returns:
        None
    """
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
