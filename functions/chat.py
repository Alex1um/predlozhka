
from aiogram.types import Message
from dispatcher import dp
from bot import bot
from aiogram import F
from aiogram.filters import CommandStart, Command
from database import database as db
from redis.commands.json.path import Path
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, ChatMemberMember, ChatMemberOwner, ChatMemberAdministrator, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class PostForm(StatesGroup):
    channel = State()
    post = State()

@dp.message(CommandStart())
async def on_start(msg: Message, state: FSMContext):
    await state.clear()
    db.set(f"user:{msg.from_user.id}", msg.chat.id)
    return msg.answer("Добро пожаловать", reply_markup=ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="Предложить пост")
        ]
    ]))

@dp.message(Command("cancel"))
@dp.message(Command("reset"))
async def on_reset(msg: Message, state: FSMContext):
    await state.clear()
    return msg.answer("Сброс...", reply_markup=ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="Предложить пост")
        ]
    ]))

@dp.message(F.text == "Предложить пост")
async def on_conv_start(msg: Message, state: FSMContext):
    channels = db.scan(match="channel:*:admins")
    channel_list = InlineKeyboardBuilder()
    channel: bytes
    for channel in channels[1]:
        fst = channel.find(ord(":"))
        scnd = channel.find(ord(":"), fst + 1)
        chat_id = channel[fst + 1:scnd]
        status = await bot.get_chat_member(chat_id, msg.from_user.id)
        if isinstance(status, (ChatMemberMember, ChatMemberAdministrator, ChatMemberOwner)):
            channel_list.button(text=chat_id, callback_data=chat_id)
    channel_list.adjust(1, repeat=True)
    await state.set_state(PostForm.channel)
    return msg.answer("Выберите канал", reply_markup=channel_list.as_markup())

@dp.message(PostForm.channel)
async def on_chat_id(msg: Message, state: FSMContext):
    await state.update_data(channel = msg.text)
    await state.set_state(PostForm.post)
    return msg.answer("Создайте пост в следущем сообщении")

@dp.message(PostForm.post)
async def on_post(msg: Message, state: FSMContext):
    # Проверка поста
    if True:
        data = await state.get_data()
        channel_id = data.channel
        admins = db.get(f"channel:{channel_id}:admins")
        for admin_id in admins:
            if (admin_chat := db.get(f"user:{admin_id}")) is not None:
                await bot.send_message(admin_chat, msg.text)
        await msg.forward(channel_id)
        await state.clear()
        
        return msg.answer("Пост предложен", reply_markup=ReplyKeyboardMarkup(keyboard=[
            [
                KeyboardButton(text="Предложить пост")
            ]
        ]))
    else:
        return msg.answer("Пост не прошел проверку. Создайте новый пост в следущем сообщении или обновите старый")

