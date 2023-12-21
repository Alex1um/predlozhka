
from aiogram.types import Message
from dispatcher import dp
from bot import bot

@dp.message()
async def on_msg(msg: Message):
    me = await bot.get_me()
    print("123", msg.text)