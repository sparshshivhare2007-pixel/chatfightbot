from PIL import Image, ImageDraw, ImageFont
from ui.themes import BAR_COLOR
import os

BASE_DIR = os.path.dirname(__file__)

FONT_PATH = os.path.join(BASE_DIR, "fonts", "regular.ttf")
BG_PATH = os.path.join(BASE_DIR, "templates", "leaderboard_bg.png")


async def generate_leaderboard_image(data, title="LEADERBOARD"):

    if os.path.exists(BG_PATH):
        img = Image.open(BG_PATH).convert("RGB")
    else:
        img = Image.new("RGB", (800, 600), (30, 30, 30))

    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype(FONT_PATH, 28)
    except:
        font = ImageFont.load_default()

    draw.text((50, 30), title, font=font, fill=(255, 255, 255))

    if not data:
        img.save("leaderboard.png")
        return "leaderboard.png"

    max_score = max(score for _, score in data)

    y = 100
    for i, (member, score) in enumerate(data, start=1):

        bar_width = int((score / max_score) * 500) if max_score > 0 else 0

        draw.text((50, y), f"{i}. {member}", font=font, fill=(255, 255, 255))

        draw.rectangle(
            [(300, y + 10), (300 + bar_width, y + 40)],
            fill=BAR_COLOR
        )

        draw.text(
            (300 + bar_width + 10, y + 10),
            str(int(score)),
            font=font,
            fill=(255, 255, 255)
        )

        y += 50

    output_path = "leaderboard.png"
    img.save(output_path)

    return output_path
