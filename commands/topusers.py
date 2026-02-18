from pyrogram import filters
from pyrogram.handlers import MessageHandler
from services.leaderboard_service import get_global_top
from ui.keyboards import ranking_keyboard
from services.formatting_service import format_leaderboard

async def topusers_cmd(client, message):

    data = await get_global_top("overall")
    text = await format_leaderboard(data, "GLOBAL LEADERBOARD")

    await message.reply(
        text,
        reply_markup=ranking_keyboard("overall", "global", 0)
    )

topusers_handler = MessageHandler(topusers_cmd, filters.command("topusers"))
