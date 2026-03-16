import asyncio
from pyrogram import Client, filters
from pytgcalls import GroupCallFactory
from pytgcalls.types.input_stream import AudioPiped
from yt_dlp import YoutubeDL
from config import API_ID, API_HASH, BOT_TOKEN
import os

# Klasör
DOWNLOAD_DIR = "downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Telegram Client
bot = Client(
    "iso_music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Yeni PyTgCalls yerine GroupCallFactory
group_call_factory = GroupCallFactory(bot)
queues = {}

# YoutubeDL ayarları
ytdl_opts = {
    "format": "bestaudio",
    "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
    "quiet": True
}

def download_song(query):
    with YoutubeDL(ytdl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)["entries"][0]
        file = ydl.prepare_filename(info)
    return file, info["title"]

# Komutlar
@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "✨ **ISO. Music Bot**\n\n"
        "▶ /play şarkı\n⏸ /pause\n▶ /resume\n⏭ /skip\n⏹ /stop\n📜 /queue\n👋 /leave"
    )

@bot.on_message(filters.command("play"))
async def play(client, message):
    if len(message.command) < 2:
        return await message.reply("⚠️ Şarkı adı yaz!")
    query = message.text.split(None,1)[1]
    msg = await message.reply("🔎 Şarkı aranıyor...")

    file, title = download_song(query)
    chat_id = message.chat.id
    if chat_id not in queues:
        queues[chat_id] = []

    queues[chat_id].append((file,title))

    if len(queues[chat_id]) == 1:
        # Voice chat’e katıl ve çal
        call = group_call_factory.get_file_group_call()
        await call.start(chat_id)
        await call.stream(AudioPiped(file))
        await msg.edit(f"🎶 **Çalıyor:** {title}")
    else:
        await msg.edit(f"📥 **Queue eklendi:** {title}")

@bot.on_message(filters.command("stop"))
async def stop(client, message):
    chat_id = message.chat.id
    if chat_id in queues:
        queues[chat_id] = []
    call = group_call_factory.get_file_group_call()
    await call.stop()
    await message.reply("⏹ **Müzik durduruldu**")

# Bot çalıştırma
async def main():
    await bot.start()
    print("ISO Music Bot aktif")
    await asyncio.Event().wait()

asyncio.run(main())
