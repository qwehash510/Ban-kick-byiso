import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ChatMemberAdministrator, ChatMemberOwner

TOKEN = "8632170346:AAEyem9RE5gM7HQXwoSAnaL0m8rpE5vbpWA"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def is_admin(chat_id, user_id):
    member = await bot.get_chat_member(chat_id, user_id)
    return isinstance(member, (ChatMemberAdministrator, ChatMemberOwner))


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("iso7K aktif. ⚡")


@dp.message(Command("banall"))
async def ban_all(message: types.Message):

    if not await is_admin(message.chat.id, message.from_user.id):
        return await message.answer("Bu komutu sadece admin kullanabilir.")

    await message.answer("Her mısırın bir firavunu var by iso7K ⚡")

    try:
        members = []
        async for m in bot.get_chat_administrators(message.chat.id):
            members.append(m.user.id)

        async for user in bot.get_chat_members(message.chat.id):
            if user.user.id in members:
                continue

            try:
                await bot.ban_chat_member(message.chat.id, user.user.id)
            except:
                pass

        await message.answer("C7K ve Tafa sunar.")

    except Exception as e:
        await message.answer("Hata oluştu.")
        print(e)


@dp.message(Command("kickall"))
async def kick_all(message: types.Message):

    if not await is_admin(message.chat.id, message.from_user.id):
        return await message.answer("Bu komutu sadece admin kullanabilir.")

    await message.answer("Her mısırın bir firavunu var by iso7K ⚡")

    try:
        admins = []
        async for m in bot.get_chat_administrators(message.chat.id):
            admins.append(m.user.id)

        async for user in bot.get_chat_members(message.chat.id):
            if user.user.id in admins:
                continue

            try:
                await bot.ban_chat_member(message.chat.id, user.user.id)
                await bot.unban_chat_member(message.chat.id, user.user.id)
            except:
                pass

        await message.answer("C7K ve Tafa sunar.")

    except Exception as e:
        await message.answer("Hata oluştu.")
        print(e)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
