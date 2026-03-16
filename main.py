import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from yt_dlp import YoutubeDL
from config import API_ID, API_HASH, BOT_TOKEN

DOWNLOAD_DIR = "downloads"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

bot = Client(
    "iso_music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call = PyTgCalls(bot)

queues = {}

ytdl_opts = {
    "format": "bestaudio",
    "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
    "quiet": True,
}

def download_song(query):

    with YoutubeDL(ytdl_opts) as ydl:

        info = ydl.extract_info(f"ytsearch:{query}", download=True)["entries"][0]
        file = ydl.prepare_filename(info)

    return file, info["title"]


@bot.on_message(filters.command("start"))
async def start(client, message: Message):

    text = """
✨ **ISO. MUSIC BOT**

🎧 Sesli sohbette müzik çalar

**Komutlar**

▶ /play şarkı  
⏸ /pause  
▶ /resume  
⏭ /skip  
⏹ /stop  
📜 /queue  
👋 /leave
"""

    await message.reply_text(text)


@bot.on_message(filters.command("play"))
async def play(client, message: Message):

    if len(message.command) < 2:
        return await message.reply("⚠️ **Şarkı adı yaz!**")

    query = message.text.split(None,1)[1]

    msg = await message.reply("🔎 **Şarkı aranıyor...**")

    file, title = download_song(query)

    chat_id = message.chat.id

    if chat_id not in queues:
        queues[chat_id] = []

    queues[chat_id].append((file,title))

    if len(queues[chat_id]) == 1:

        await call.join_group_call(
            chat_id,
            AudioPiped(file)
        )

        await msg.edit(f"🎶 **Çalıyor:** {title}")

    else:

        await msg.edit(f"📥 **Queue eklendi:** {title}")


@bot.on_message(filters.command("skip"))
async def skip(client, message: Message):

    chat_id = message.chat.id

    if chat_id not in queues or len(queues[chat_id]) < 2:
        return await message.reply("⚠️ **Atlanacak şarkı yok**")

    queues[chat_id].pop(0)

    file,title = queues[chat_id][0]

    await call.change_stream(
        chat_id,
        AudioPiped(file)
    )

    await message.reply(f"⏭ **Atlandı**\n🎶 {title}")


@bot.on_message(filters.command("pause"))
async def pause(client, message: Message):

    await call.pause_stream(message.chat.id)

    await message.reply("⏸ **Müzik duraklatıldı**")


@bot.on_message(filters.command("resume"))
async def resume(client, message: Message):

    await call.resume_stream(message.chat.id)

    await message.reply("▶ **Müzik devam ediyor**")


@bot.on_message(filters.command("stop"))
async def stop(client, message: Message):

    queues[message.chat.id] = []

    await call.leave_group_call(message.chat.id)

    await message.reply("⏹ **Müzik durduruldu**")


@bot.on_message(filters.command("queue"))
async def queue(client, message: Message):

    chat_id = message.chat.id

    if chat_id not in queues or not queues[chat_id]:
        return await message.reply("📭 **Queue boş**")

    text = "📜 **Müzik Listesi**\n\n"

    for i,(file,title) in enumerate(queues[chat_id]):
        text += f"{i+1}. {title}\n"

    await message.reply(text)


@bot.on_message(filters.command("leave"))
async def leave(client, message: Message):

    await call.leave_group_call(message.chat.id)

    await message.reply("👋 **Sohbetten çıktım**")


async def main():

    await bot.start()
    await call.start()

    print("ISO MUSIC BOT AKTİF")

    await asyncio.Event().wait()

asyncio.run(main())
