from aiogram.types import Message
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ChatMemberMember,
    ChatMemberOwner,
    ChatMemberAdministrator,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from text_classificator.instance import get_translated
from dispatcher import dp
from bot import bot
from database import database as db


class PostForm(StatesGroup):
    channel = State()
    post = State()


@dp.message(CommandStart())
async def on_start(msg: Message, state: FSMContext):
    await state.clear()
    return msg.answer(
        "Добро пожаловать",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Предложить пост")]]
        ),
    )


@dp.message(Command("cancel"))
@dp.message(Command("reset"))
async def on_reset(msg: Message, state: FSMContext):
    await state.clear()
    return msg.answer(
        "Сброс...",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Предложить пост")]]
        ),
    )


@dp.message(F.text == "Предложить пост")
async def on_conv_start(msg: Message, state: FSMContext):
    channels = db.scan(match="channel:*:admins")
    channel_list = InlineKeyboardBuilder()
    channel: bytes
    is_any_channel = False
    for channel in channels[1]:
        fst = channel.find(ord(":"))
        scnd = channel.find(ord(":"), fst + 1)
        chat_id = channel[fst + 1: scnd]
        name = db.get(channel[:scnd] + b":name")
        if name is None:
            name = chat_id
        try:
            status = await bot.get_chat_member(chat_id, msg.from_user.id)
            if isinstance(
                status, (ChatMemberMember,
                         ChatMemberAdministrator, ChatMemberOwner)
            ):
                channel_list.button(text=name, callback_data=chat_id)
                is_any_channel = True
        except Exception:
            pass
    if not is_any_channel:
        return msg.answer("Нет доступных каналов")
    channel_list.adjust(1, repeat=True)
    await state.set_state(PostForm.channel)
    return msg.answer("Выберите канал", reply_markup=channel_list.as_markup())


@dp.callback_query(PostForm.channel)
async def on_callback_chat_id(cq: CallbackQuery, state: FSMContext):
    channel_id = cq.data
    name: bytes = db.get(f"channel:{channel_id}:name")
    if name is None:
        name = channel_id
    await state.update_data(channel=cq.data)
    await state.set_state(PostForm.post)
    await bot.send_message(cq.message.chat.id, "Создайте пост в следущем сообщении")
    await cq.answer(f"Выбран чат {name.decode('utf-8')}")


@dp.message(PostForm.post)
async def on_post(msg: Message, state: FSMContext):
    # Проверка поста
    if True:
        data = await state.get_data()
        channel_id = data["channel"]
        admins = db.smembers(f"channel:{channel_id}:admins")
        name: bytes = db.get(f"channel:{channel_id}:name")
        if name is None:
            name = channel_id
        # theme = get_translated(msg.text)
        translate, prob = get_translated(msg.text)
        for admin_id in admins:
            try:
                await bot.send_message(
                    admin_id,
                    f"Новый пост в {name.decode('utf-8')} от {msg.from_user.first_name}\nТема: {translate} с вероятностью {int(prob * 100)}%",
                )
                await msg.send_copy(
                    admin_id,
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text=f"Опубликовать в {name.decode('utf-8')}",
                                    callback_data=f"{channel_id}",
                                )
                            ]
                        ]
                    ),
                )
            except Exception:
                pass
        await state.clear()

        return msg.answer(
            "Пост предложен",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="Предложить пост")]]
            ),
        )
    else:
        return msg.answer(
            "Пост не прошел проверку. Создайте новый пост в следущем сообщении или обновите старый"
        )


@dp.callback_query()
async def on_callback_publish(cq: CallbackQuery, _: FSMContext):
    channel_to_publish = cq.data
    name: bytes = db.get(f"channel:{channel_to_publish}:name")
    if name is None:
        name = channel_to_publish
    await cq.message.edit_reply_markup(reply_markup=None)
    msg = await cq.message.send_copy(channel_to_publish)
    await msg.edit_reply_markup(None)
    return cq.answer(f"Опубликованно в {name.decode('utf-8')}")
