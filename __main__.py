from aiogram import Dispatcher, Bot
import asyncio
from os import getenv
from aiogram.types import Message

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher(name=__name__)
bot = Bot(TOKEN, parse_mode="HTML")

@dp.message()
async def on_msg(msg: Message):
    me = await bot.get_me()
    print("123", msg.text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())