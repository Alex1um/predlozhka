from dispatcher import dp
from aiogram import F
from .database import save_database, load_database

@dp.message(F.text == "save")
async def on_save(_):
    save_database()

@dp.message(F.text == "load")
async def on_load(_):
    load_database()