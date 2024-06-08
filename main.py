import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram import html
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.utils.formatting import Text, Bold

from group_handle import group_handle

# from config import TOKEN
from config_reader import config

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота


# Для записей с типом Secret* необходимо
# вызывать метод get_secret_value(),
# чтобы получить настоящее содержимое вместо '*******'
bot = Bot(token=config.bot_token.get_secret_value())

# bot = Bot(token=TOKEN)
# Диспетчер
dp = Dispatcher()

dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

"""
@dp.message(F.text, Command("test"))
async def any_message(message: Message):
    await message.answer("Hello, <b> world<b>", parse_mode=ParseMode.HTML)


# @dp.message(Command("hello"))
async def cmd_hello(message: Message):
    await message.answer(
        f"Hello, <b>{message.from_user.full_name}</b>",
        parse_mode=ParseMode.HTML
    )


# ekranirivat
# @dp.message(Command("hello"))
async def cmd_hello(message: Message):
    await message.answer(
        f"Hello, {html.bold(html.quote(message.from_user.full_name))}",
        parse_mode=ParseMode.HTML
    )

# 2-ekranit
# @dp.message(Command("hello"))
async def cmd_hello(message: Message):
    content = Text(
        "Hello, ",
        Bold(message.from_user.full_name)
    )
    await message.answer(
        **content.as_kwargs()
    )

@dp.message(Command("add_to_list"))
async def cmd_add_to_list(message: types.Message, mylist: list[int]):
    mylist.append(7)

    async def cmd_hello(message: Message):

        await message.answer("Добавлено число 7")


@dp.message(Command("show_list"))
async def cmd_show_list(message: types.Message, mylist: list[int]):
    await message.answer(f"Ваш список: {mylist}")


@dp.message(Command("info"))
async def cmd_info(message: types.Message, started_at: str):
    await message.answer(f"Бот запущен {started_at}")

"""


# Хэндлер на команду /start
@dp.message(F.chat.type == "private", Command("start"))
async def cmd_start(message: types.Message):
    print(message.chat.type)
    await message.answer("Hello!")


# Запуск процесса поллинга новых апдейтов
async def main():
    dp.include_router(group_handle.router)
    # await dp.start_polling(bot)
    await dp.start_polling(bot, mylist=[1, 2, 3])


if __name__ == "__main__":
    asyncio.run(main())
