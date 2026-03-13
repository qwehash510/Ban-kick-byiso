import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Basit HTTP server (Railway Web Service için)
async def keep_alive():
    async def handler(request):
        return web.Response(text="Bot çalışıyor!")
    app = web.Application()
    app.add_routes([web.get("/", handler)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", 8000)))
    await site.start()

# Hızlı ban fonksiyonu
async def fast_ban(chat_id: int, user_id: int):
    try:
        await bot.ban_chat_member(chat_id, user_id)
    except:
        pass

# /ban komutu
@dp.message(Command("ban"))
async def ban_command(message: types.Message):
    try:
        limit = int(message.text.split()[1])
    except:
        await message.answer("Kullanım: /ban 100")
        return

    banned = 0
    tasks = []

    async for member in bot.iter_chat_members(message.chat.id):
        if banned >= limit:
            break
        if member.user.is_bot:
            continue
        tasks.append(fast_ban(message.chat.id, member.user.id))
        banned += 1

        # 50 kişi bir dalga
        if len(tasks) >= 50:
            await asyncio.gather(*tasks)
            tasks = []

    if tasks:
        await asyncio.gather(*tasks)

    await message.answer("iso7K farkıyla")

# Başlangıç mesajı
async def on_startup():
    print("her mısırın bir firavunu var")
    print("Railway’de hatasız çalıştı")

# Main
async def main():
    await keep_alive()
    await on_startup()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
