import discord
import asyncio
import aiohttp
import random
import time
import requests
import threading
from websockets.asyncio.server import serve

import os
import dotenv
import sys

dotenv.load_dotenv()

from discord.ext.commands import Bot

from discord.ext import tasks

command_prefix="!"
description="Hello, World!"

run_thread = True

intents = discord.Intents.all()
bot = Bot(command_prefix=command_prefix, description=description, intents=intents)
client = discord.Client(intents=intents)
game = discord.Game("!info")

dm_channel = None

@bot.event
async def on_ready(client=client, game=game):
    global dm_channel
    print("Logged in.")
    await bot.change_presence(activity=game)
    dm_channel = await bot.fetch_channel(os.getenv("DISCORD_TEST_DM_TARGET"))
    asyncio.get_event_loop().create_task(ws_handle())


    
@bot.event
async def on_message(message):
    print(f"Received message {message.content}")

async def wrapper_send(content):
    global dm_channel

    await dm_channel.send(f"{content}")
    
async def send_dm_no_ctx(websocket):
    global client, bot, dm_channel, client_loop

    
    
    out = ""
    last_msg = await websocket.recv()
    out = last_msg
    print(f"(II) Sending msg to dm: {out}")

    if dm_channel is not None:
        await dm_channel.send(f"{out}")
    else:
        print("No channel registered or channel invalid")

async def ws_handle():
    print("toto")
    async with serve(send_dm_no_ctx, "localhost", 8765) as server:
        await server.serve_forever()

if __name__ == '__main__':
    token = os.getenv("DISCORD_TOKEN")
    bot.run(token)


    # bot.run(token)
