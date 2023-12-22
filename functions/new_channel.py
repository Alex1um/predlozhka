from dispatcher import dp
from database import database
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, ADMINISTRATOR
from aiogram.types import ChatMemberUpdated
from bot import bot

@dp.my_chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> ADMINISTRATOR))
async def on_new_channel(upd: ChatMemberUpdated):
    admins = await upd.chat.get_administrators()
    admins_ids = map(lambda x: x.user.id, admins)
    database.sadd(f"channel:{upd.chat.id}:admins", *admins_ids)
    print("new chat!")
