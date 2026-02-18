from pyrogram import filters
from pyrogram.handlers import MessageHandler
from services.leaderboard_service import get_group_top
from ui.keyboards import ranking_keyboard
from services.formatting_service import format_leaderboard

async def rankings_cmd(client, message):

    if message.chat.type not in ["group", "supergroup"]:
        return

    data = await get_group_top(message.chat.id, "overall")
    text = await format_leaderboard(data, "LEADERBOARD")

    await message.reply(
        text,
        reply_markup=ranking_keyboard("overall", "group", message.chat.id)
    )

rankings_handler = MessageHandler(rankings_cmd, filters.command("rankings"))
