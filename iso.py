import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiohttp import web

# PORT ve TOKEN
PORT = int(os.environ.get("PORT", 8000))
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Hızlı ban fonksiyonu
async def fast_ban(chat_id, user_id):
    try:
        await bot.kick_chat_member(chat_id, user_id)
    except:
        pass

# /ban komutu
@dp.message_handler(commands=["ban"])
async def ban_wave(message: types.Message):
    try:
        limit = int(message.get_args())
    except:
        return await message.reply("Kullanım: /ban 100")

    banned = 0

    # Aiogram 2.x ile üyeleri almak için get_chat_members veya get_chat_member kullanıyoruz
    members = await bot.get_chat_administrators(message.chat.id)  # Adminleri al
    admin_ids = [admin.user.id for admin in members]

    offset = 0
    while banned < limit:
        # Telegram API sadece 200 kişi çekebilir
        chunk = await bot.get_chat_members(message.chat.id, offset=offset)
        if not chunk:
            break

        for member in chunk:
            user_id = member.user.id
            if user_id in admin_ids:
                continue
            await fast_ban(message.chat.id, user_id)
            banned += 1
            if banned >= limit:
                break
        offset += len(chunk)

    await message.reply("iso7K farkıyla")

# Bot startup
async def on_startup(dp):
    print("her mısırın bir firavunu var")
    print("C7K SİKER")

# Basit HTTP server (Render Web Service için)
async def keep_alive():
    async def handler(request):
        return web.Response(text="Bot çalışıyor!")

    app = web.Application()
    app.add_routes([web.get("/", handler)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

# Polling + HTTP server
async def main():
    await keep_alive()
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
