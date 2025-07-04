from dotenv import load_dotenv

load_dotenv()

import os, sys
from bot import Bot

import asyncio

async def main():
    bot_id = os.getenv("TWITCH_BOT_ID")
    bot_secret = os.getenv("TWITCH_BOT_SECRET")
    bot = Bot(bot_id, bot_secret)

    #bot.get_new_token()
    #bot.debug_dump_token()

    #bot.send_msg("Hello, World!")

    await bot.irc_connect_to_chat_read()
    
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.create_task(main())
    loop.run_forever()
