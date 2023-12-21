from aiogram import Bot
from os import getenv

TOKEN = getenv("BOT_TOKEN")

bot = Bot(TOKEN, parse_mode="HTML")
