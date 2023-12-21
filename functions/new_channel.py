from dispatcher import dp
from database import database
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, ADMINISTRATOR
from aiogram.types import ChatMemberUpdated
from bot import bot

@dp.my_chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> ADMINISTRATOR))
async def on_new_channel(upd: ChatMemberUpdated):
    database["channels"].add(upd.chat.id)
    if upd["channel_admins"][upd.chat_id] is None:
        upd["channel_admins"][upd.chat_id] = set()
    # only for the admin who invited
    # database["admins"][upd.chat.id] = upd.from_user.id
    # or for all admins
    admins = await bot.get_chat_administrators(upd.chat.id)    
    for admin in admins:
        # add all admins to channel in database
        database["channel_admins"][upd.chat.id].add(admin.user.id)
        # add admin to admin_chats if no chat with admin yet
        if admin.user.id not in database["admin_chats"]:
            database["admin_chats"][admin.user.id] = None
        elif admin.user.id in database["user_chats"]:
            database["admin_chats"][admin.user.id] = database["user_chats"][admin.user.id]
    print("new chat!")
