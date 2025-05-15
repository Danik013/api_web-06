import os
import random
import time

import requests
import telegram
from dotenv import load_dotenv


def get_image(url):
    response = requests.get(url)
    response.raise_for_status()

    return response.content


def upload_comic(file_to_publish):
    comic_number = random.randint(1, 3090)
    url = f"https://xkcd.com/{comic_number}/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    comic_response = response.json()

    img_comic = get_image(comic_response["img"])
    with open(file_to_publish, "wb") as file:
        file.write(img_comic)

    return comic_response["alt"]


def publish_comic(chat_id, bot, comment):
    with open("xkcd.png", "rb") as file:
        bot.send_photo(chat_id=chat_id, photo=file, caption=comment)


def main():
    load_dotenv()
    token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["TG_CHAT_ID"]

    bot = telegram.Bot(token=token)

    file_to_publish = "xkcd.png"

    daily_publication = 86400

    while True:
        comment = upload_comic(file_to_publish)

        publish_comic(chat_id, bot, comment)

        if os.path.exists(file_to_publish):
            os.remove(file_to_publish)

        time.sleep(daily_publication)


if __name__ == '__main__':
    main()
