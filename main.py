import os
import asyncio
from aiogram import Bot, Dispatcher, types

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def fast_ban(chat_id, user_id):
    try:
        await bot.kick_chat_member(chat_id, user_id)
    except:
        pass

@dp.message_handler(commands=["ban"])
async def ban_command(message: types.Message):
    try:
        limit = int(message.text.split()[1])
    except:
        await message.reply("Kullanım: /ban 100")
        return

    banned = 0
    admins = await bot.get_chat_administrators(message.chat.id)
    admin_ids = [a.user.id for a in admins]

    offset = 0
    while banned < limit:
        members = await bot.get_chat_members(message.chat.id, offset=offset)
        if not members:
            break

        for m in members:
            if m.user.id in admin_ids or m.user.is_bot:
                continue
            await fast_ban(message.chat.id, m.user.id)
            banned += 1
            if banned >= limit:
                break
        offset += len(members)

    await message.reply("iso7K farkıyla")

async def main():
    print("her mısırın bir firavunu var")
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
