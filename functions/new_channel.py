"""
New channel functions
"""
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, ADMINISTRATOR, IS_MEMBER
from aiogram.types import ChatMemberUpdated
from bot import bot
from dispatcher import dp
from database import database


@dp.my_chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> ADMINISTRATOR))
async def on_new_channel(upd: ChatMemberUpdated):
    """
    Handles the event when a new channel is created.

    This function is a handler for the `my_chat_member` event with the filter `ChatMemberUpdatedFilter(IS_NOT_MEMBER >> ADMINISTRATOR)`.
    It is triggered when a new channel is created and the bot is not an admin in the channel.

    Parameters:
        upd (ChatMemberUpdated): The update object containing information about the chat member update event.

    Returns:
        None

    Side Effects:
        - Retrieves the list of administrators in the channel.
        - Extracts the IDs of non-bot administrators.
        - Adds the non-bot admin IDs to the set of admins in the channel in the database.
        - Sets the name of the channel in the database.
        - Prints "new chat!" to the console.

    Note:
        - The commented out line `if upd.new_chat_member.user == bot.id:` is currently not in use.
        - The function assumes that the necessary imports (`from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, ADMINISTRATOR, IS_MEMBER`, `from aiogram.types import ChatMemberUpdated`, `from bot import bot`, `from dispatcher import dp`, `from database import database`) are present.
    """
    # if upd.new_chat_member.user == bot.id:
    admins = await upd.chat.get_administrators()
    admins_ids = (
        admin.user.id for admin in admins if admin.user.is_bot is False)
    database.sadd(f"channel:{upd.chat.id}:admins", *admins_ids)
    database.set(f"channel:{upd.chat.id}:name", upd.chat.full_name)
    print("new chat!")


@dp.my_chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> ADMINISTRATOR))
async def on_promotion(upd: ChatMemberUpdated):
    """
    Handles the event when a chat member is promoted to an admin role.

    This function is a handler for the `my_chat_member` event with the filter `ChatMemberUpdatedFilter(IS_MEMBER >> ADMINISTRATOR)`.
    It is triggered when a chat member is promoted to an admin role.

    Parameters:
        upd (ChatMemberUpdated): The update object containing information about the chat member update event.

    Returns:
        None

    Side Effects:
        - Adds the ID of the promoted member to the set of admins in the channel in the database.
        - Prints "promoted" to the console.

    Note:
        - The commented out line `if upd.new_chat_member.user == bot.id:` is currently not in use.
        - The function assumes that the necessary imports (`from aiogram.filters import ChatMemberUpdatedFilter, IS_MEMBER, ADMINISTRATOR`, `from aiogram.types import ChatMemberUpdated`, `from database import database`) are present.
    """
    # if upd.new_chat_member.user == bot.id:
    database.sadd(f"channel:{upd.chat.id}:admins", upd.new_chat_member.user.id)
    print("promoted")


@dp.my_chat_member(ChatMemberUpdatedFilter(ADMINISTRATOR >> IS_NOT_MEMBER))
@dp.my_chat_member(ChatMemberUpdatedFilter(ADMINISTRATOR >> IS_MEMBER))
async def on_demotion(upd: ChatMemberUpdated):
    """
    Handles the event when a chat member is demoted from an admin role.

    This function is a handler for the `my_chat_member` event with the filter `ChatMemberUpdatedFilter(ADMINISTRATOR >> IS_NOT_MEMBER)` and `ChatMemberUpdatedFilter(ADMINISTRATOR >> IS_MEMBER)`.
    It is triggered when a chat member is demoted from an admin role.

    Parameters:
        upd (ChatMemberUpdated): The update object containing information about the chat member update event.

    Returns:
        None

    Side Effects:
        - If the demoted member is the bot itself, the name and admin IDs of the channel in the database are deleted.
        - The ID of the demoted member is removed from the set of admins in the channel in the database.
        - Prints "removed!" to the console.

    Note:
        - The function assumes that the necessary imports (`from aiogram.filters import ChatMemberUpdatedFilter, ADMINISTRATOR, IS_NOT_MEMBER, IS_MEMBER`, `from aiogram.types import ChatMemberUpdated`, `from bot import bot`, `from database import database`) are present.
    """
    if upd.new_chat_member.user == bot.id:
        database.delete(f"channel:{upd.chat.id}:name")
        database.delete(f"channel:{upd.chat.id}:admins")
    database.srem(f"channel:{upd.chat.id}:admins", upd.new_chat_member.user.id)
    print("removed!")
