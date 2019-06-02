import textwrap
from django.conf import settings
from telegram import Bot, TelegramError
from PIL import Image, ImageDraw, ImageFont


def post_telegram_channel(message):
    if not settings.TELEGRAM_TOKEN and not settings.TELEGRAM_CHATID:
        return False, "missing_auth_keys"

    bot = Bot(settings.TELEGRAM_TOKEN)
    try:
        bot.send_message(chat_id=settings.TELEGRAM_CHATID, text=message)
    except TelegramError:
        return False, "wrong_auth_keys"

    return True, "success"


def generate_thumbnail(job):
    font_path = "{}Montserrat/Montserrat-Medium.ttf".format(
        settings.THUMBNAILS_BASE_FOLDER
    )
    font_bold_path = "{}Montserrat/Montserrat-Bold.ttf".format(
        settings.THUMBNAILS_BASE_FOLDER
    )

    font_med_cntr = ImageFont.truetype(font_path, 60)
    font_bold_cntr = ImageFont.truetype(font_bold_path, 60)

    im = Image.open("{}thumb_base.png".format(settings.THUMBNAILS_BASE_FOLDER))
    im = im.resize((1280, 720))

    mask = Image.new("L", im.size, color=0)
    draw = ImageDraw.Draw(mask)
    transparent_area = (0, 0, 1280, 720)

    draw.rectangle(transparent_area, fill=30)
    im.putalpha(mask)

    draw = ImageDraw.Draw(im)

    w, _ = draw.textsize("Nova Oportunidade:", font=font_med_cntr)
    draw.text(
        ((1280 - w) / 2, 90),
        text="Nova Oportunidade:",
        fill="white",
        font=font_med_cntr,
    )

    offset = 225
    for line in textwrap.wrap(job.title, width=25):
        w, _ = draw.textsize(line, font=font_bold_cntr)
        draw.text(((1280 - w) / 2, offset), line, font=font_bold_cntr)
        offset += font_bold_cntr.getsize(line)[1]

    w, _ = draw.textsize("Via PyJobs", font=font_med_cntr)
    draw.text(
        ((1280 - w) / 2, 500), text="Via PyJobs", fill="white", font=font_med_cntr
    )

    return im
