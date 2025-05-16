import os
import random
import time

import requests
import telegram
from dotenv import load_dotenv


COMICS_FILENAME = "xkcd.png"
COMICS_MIN_NUMBER = 1
COMICS_MAX_NUMBER = 3090


def upload_comics(file_to_publish, comics_number):
    url = f"https://xkcd.com/{comics_number}/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    comics_response = response.json()

    response = requests.get(comics_response["img"])
    response.raise_for_status()

    with open(file_to_publish, "wb") as file:
        file.write(response.content)

    return comics_response["alt"]


def publish_comics(chat_id, bot, comment):
    with open(COMICS_FILENAME, "rb") as file:
        bot.send_photo(chat_id=chat_id, photo=file, caption=comment)


def main():
    load_dotenv()
    token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["TG_CHAT_ID"]

    bot = telegram.Bot(token=token)

    daily_publication = 86400

    while True:
        comics_number = random.randint(COMICS_MIN_NUMBER, COMICS_MAX_NUMBER)
        comment = upload_comics(COMICS_FILENAME, comics_number)

        publish_comics(chat_id, bot, comment)

        if os.path.exists(COMICS_FILENAME):
            os.remove(COMICS_FILENAME)

        time.sleep(daily_publication)


if __name__ == '__main__':
    main()
