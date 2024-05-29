"""
Create bot
"""
from os import getenv
from aiogram import Bot

TOKEN = getenv("BOT_TOKEN")

bot = Bot(TOKEN, parse_mode="HTML")
