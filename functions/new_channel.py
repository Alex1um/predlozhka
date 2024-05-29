from dispatcher import dp
from database import database
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, ADMINISTRATOR, IS_MEMBER
from aiogram.types import ChatMemberUpdated
from bot import bot


@dp.my_chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> ADMINISTRATOR))
async def on_new_channel(upd: ChatMemberUpdated):
    # if upd.new_chat_member.user == bot.id:
    admins = await upd.chat.get_administrators()
    admins_ids = (
        admin.user.id for admin in admins if admin.user.is_bot is False)
    database.sadd(f"channel:{upd.chat.id}:admins", *admins_ids)
    database.set(f"channel:{upd.chat.id}:name", upd.chat.full_name)
    print("new chat!")


@dp.my_chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> ADMINISTRATOR))
async def on_promotion(upd: ChatMemberUpdated):
    # if upd.new_chat_member.user == bot.id:
    database.sadd(f"channel:{upd.chat.id}:admins", upd.new_chat_member.user.id)
    print("promoted")


@dp.my_chat_member(ChatMemberUpdatedFilter(ADMINISTRATOR >> IS_NOT_MEMBER))
@dp.my_chat_member(ChatMemberUpdatedFilter(ADMINISTRATOR >> IS_MEMBER))
async def on_demotion(upd: ChatMemberUpdated):
    if upd.new_chat_member.user == bot.id:
        database.delete(f"channel:{upd.chat.id}:name")
        database.delete(f"channel:{upd.chat.id}:admins")
    database.srem(f"channel:{upd.chat.id}:admins", upd.new_chat_member.user.id)
    print("removed!")
