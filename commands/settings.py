from pyrogram import filters
from pyrogram.handlers import MessageHandler

async def settings_cmd(client, message):
    await message.reply("⚙ Settings coming soon.")

settings_handler = MessageHandler(settings_cmd, filters.command("settings"))
