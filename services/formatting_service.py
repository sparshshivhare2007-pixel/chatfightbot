def format_number(num):
    return "{:,}".format(int(num)).replace(",", ".")


async def format_leaderboard(data, title):

    text = f"🏆 {title}\n\n"

    if not data:
        return text + "No data yet."

    for i, (member, score) in enumerate(data, start=1):
        text += f"{i}. {member} • {format_number(score)}\n"

    return text
