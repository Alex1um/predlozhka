
from aiogram.types import Message
from dispatcher import dp
from bot import bot
from aiogram import F
from aiogram.filters import CommandStart, Command
from database import database as db
from redis.commands.json.path import Path
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, ChatMemberMember, ChatMemberOwner, ChatMemberAdministrator, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Update
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class PostForm(StatesGroup):
    channel = State()
    post = State()

@dp.message(CommandStart())
async def on_start(msg: Message, state: FSMContext):
    await state.clear()
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
    is_any_channel = False
    for channel in channels[1]:
        fst = channel.find(ord(":"))
        scnd = channel.find(ord(":"), fst + 1)
        chat_id = channel[fst + 1:scnd]
        try:
            status = await bot.get_chat_member(chat_id, msg.from_user.id)
            if isinstance(status, (ChatMemberMember, ChatMemberAdministrator, ChatMemberOwner)):
                channel_list.button(text=chat_id, callback_data=chat_id)
                is_any_channel = True
        except Exception as e:
            pass
    if not is_any_channel:
        return msg.answer("Нет доступных каналов")
    channel_list.adjust(1, repeat=True)
    await state.set_state(PostForm.channel)
    return msg.answer("Выберите канал", reply_markup=channel_list.as_markup())

@dp.callback_query(PostForm.channel)
async def on_callback_chat_id(cq: CallbackQuery, state: FSMContext):
    await state.update_data(channel = cq.data)
    await state.set_state(PostForm.post)
    await bot.send_message(cq.message.chat.id, "Создайте пост в следущем сообщении")
    await cq.answer(f"Выбран чат {cq.data}")

@dp.message(PostForm.post)
async def on_post(msg: Message, state: FSMContext):
    # Проверка поста
    if True:
        data = await state.get_data()
        channel_id = data['channel']
        admins = db.smembers(f"channel:{channel_id}:admins")
        for admin_id in admins:
            try:
                await msg.send_copy(admin_id, reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text=f"Опубликовать в {channel_id}", callback_data=f"{channel_id}")
                    ]
                ]))
            except Exception as e:
                pass
        await state.clear()
        
        return msg.answer("Пост предложен", reply_markup=ReplyKeyboardMarkup(keyboard=[
            [
                KeyboardButton(text="Предложить пост")
            ]
        ]))
    else:
        return msg.answer("Пост не прошел проверку. Создайте новый пост в следущем сообщении или обновите старый")


@dp.callback_query()
async def on_callback_publish(cq: CallbackQuery, state: FSMContext):
    channel_to_publish = cq.data
    await cq.message.edit_reply_markup(reply_markup=None)
    msg = await cq.message.send_copy(cq.data)
    await msg.edit_reply_markup(None)
    return cq.answer(f"Опубликованно в {channel_to_publish}")