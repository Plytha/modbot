from dotenv import load_dotenv

load_dotenv()

import os, sys
from bot import Bot


def main():
    bot_id = os.getenv("TWITCH_BOT_ID")
    bot_secret = os.getenv("TWITCH_BOT_SECRET")
    bot = Bot(bot_id, bot_secret)

    bot.get_new_token()
    bot.debug_dump_token()

    bot.send_msg("Hello, World!")

    bot.start_reading_chat()
    
if __name__ == "__main__":
    main()
