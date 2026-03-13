import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = "BOT_TOKEN"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def fast_ban(chat_id, user_id):
    try:
        await bot.ban_chat_member(chat_id, user_id)
    except:
        pass


@dp.message_handler(commands=["ban"])
async def ban_wave(message: types.Message):

    try:
        limit = int(message.get_args())
    except:
        return await message.reply("Kullanım: /ban 100")

    tasks = []
    banned = 0

    async for member in bot.iter_chat_members(message.chat.id):

        if banned >= limit:
            break

        user_id = member.user.id

        tasks.append(fast_ban(message.chat.id, user_id))
        banned += 1

        # paralel ban dalgası
        if len(tasks) >= 40:
            await asyncio.gather(*tasks)
            tasks = []

    if tasks:
        await asyncio.gather(*tasks)

    await message.reply("iso7K farkıyla")


async def on_startup(dp):
    print("her mısırın bir firavunu var")
    print("C7K farkıyla.")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
