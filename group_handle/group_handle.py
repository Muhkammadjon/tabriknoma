import asyncio
import datetime

from aiogram import F
from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types.message import Message

from main import bot
from mysql import AsyncMySQLConnector

router = Router()

name = ["ism familiya"]

connector = AsyncMySQLConnector(host='localhost', user='root', password='ubuntu', database='bot')


# await connector.connect()

# async def group_adding():
#     connector = AsyncMySQLConnector(host='localhost', user='root', password='ubuntu', database='bot')
#     await connector.connect()
#     print("connect")
#
#     data = {'group_id': 1, 'group_name': 'name', }
#     await connector.insert_data('Groups', data)
#     print("data")
#
#     await connector.disconnect()


async def loop(chat_id):
    while True:
        now = datetime.datetime.now()
        # print(now)
        await connector.connect()
        data = await connector.select_data('People', where={'data_month': f'{now.month}', 'data_day': f'{now.day}'})
        # data_name = data[0]
        # print(data)
        if len(data) == 0:
            await asyncio.sleep(86400)
        else:
            # print('else')
            while now.hour <= 10:
                await asyncio.sleep(60)
            for data_name in data:
                print(data_name)
                await bot.send_message(chat_id=chat_id, text=f"Sizni tug'ulgan kiningiz biln tabriklayman{data_name['name']}")
            # print(data['name'])
            await asyncio.sleep(86400)
        # people_day = 25
        # people_month = 4

        # if now.month == people_month and now.day == people_day:
        #     print("1")
        #     while now.hour <= 10:
        #         print("loop")
        #         time.sleep(60)
        #     await bot.send_message(chat_id=chat_id, text="mana ishladi ")
        # else:
        #     time.sleep(86400)

        # soat = now.replace(hour=14, minute=19, second=0, microsecond=0)
        # print(soat)
        #
        # if now > soat:
        #     soat += datetime.timedelta(days=1)
        #
        # while now < soat:
        #     time.sleep(1)  # 86400 s = 1 day
        #     print("loop")
        #     now = datetime.datetime.now()

        # await bot.send_message(chat_id=chat_id, text=f"Assalomu aleykum Tabriklaymiz{name[0]}")

        print("ishladi")


@router.message(F.chat.type == "group", Command("hello"))
async def cmd_hello(message: Message):
    # print(message.chat)
    # await message.answer(
    #     f"Hello, {message.from_user.full_name}")
    await loop(message.chat.id)


@router.message(F.chat.type == "group", Command("add_group"))
async def add_group(message: Message):
    print(message.chat)
    await message.answer(
        f"Group added")
    # await loop(message.chat.id)
