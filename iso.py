# iso.py — Render + Python 3.11.11 + ultra hızlı ban botu

import asyncio
import random
import logging
import os
from datetime import datetime, timedelta
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.errors import FloodWait, RPCError, UserAdminInvalid, BadRequest

# Render Environment'dan çek (hardcoded token yok!)
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN Render Environment'a eklenmemiş! Dashboard → Environment Variables'a koy.")

DELAY_MIN  = 0.055
DELAY_MAX  = 0.11
BATCH_SIZE = 120
BATCH_MOLA = 0.9

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")
LOGGER = logging.getLogger("iso")

iso = Client("iso_anarchy", bot_token=BOT_TOKEN)

attack_running = False
banned_total = 0

def is_real(u):
    return (
        not u.is_bot and
        not u.is_deleted and
        not u.is_restricted and
        u.username and len(u.username) >= 5 and
        u.photo
    )

async def nuke(chat_id: int, target: int):
    global attack_running, banned_total
    attack_running = True
    banned_total = 0

    async for member in iso.get_chat_members(chat_id):
        if not attack_running or banned_total >= target:
            break

        u = member.user
        if not is_real(u):
            continue

        try:
            await iso.ban_chat_member(chat_id, u.id)
            banned_total += 1
            LOGGER.info(f"BAN → @{u.username or u.id} [{banned_total}]")
            await asyncio.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

            if banned_total % BATCH_SIZE == 0:
                await asyncio.sleep(BATCH_MOLA)

        except FloodWait as e:
            await asyncio.sleep(e.value + 1.0)
        except Exception:
            continue

    attack_running = False
    await iso.send_message(chat_id, "her mısırın bir firavunu vardır by iso7K")

@iso.on_message(filters.command("ban") & filters.group)
async def ban_command(_, msg: Message):
    global attack_running
    if attack_running:
        return

    try:
        _, adet_str = msg.text.split(maxsplit=1)
        adet = int(adet_str)
        if adet < 100:
            return
    except:
        return

    await msg.reply("iso", quote=False)
    asyncio.create_task(nuke(msg.chat.id, adet))

async def main():
    print("iso ANARCHY MOD AKTİF - /ban sayı yaz yeter")
    await iso.start()
    await asyncio.Event().wait()  # sonsuz bekle

if __name__ == "__main__":
    asyncio.run(main())
