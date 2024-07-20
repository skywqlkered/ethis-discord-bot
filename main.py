import os
import json
from PIL import Image
from io import BytesIO
import requests

import discord
from dotenv import load_dotenv
import configparser
import dropbox

from functions.admin import *
from functions.validation import *
from functions.json import *
from functions.dropbox import *

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
client = discord.Client(intents=intents)


def gather_configini() -> configparser.ConfigParser:
    global current_guild
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config


def request_option(config_option: str):
    config: configparser.ConfigParser = gather_configini()
    return config.get("CHANNEL", config_option)


async def get_previous(message: discord.message):
    previous_msg = None
    config = gather_configini()
    staff_channel: discord.channel = await client.fetch_channel(
        int(request_option("staff_channel"))
    )
    async for msg in staff_channel.history(limit=1):
        previous_msg = msg
        break
    return previous_msg


async def send_png(message: discord.Message) -> bool:
    # check if message attch is a png
    png: discord.Attachment = get_pngs(message)[0]
    texture_url = png.url.split("?ex")[0]

    request_option("staff_channel")
    staff_channel: discord.channel = await client.fetch_channel(
        int(request_option("staff_channel"))
    )
    await staff_channel.send(
        f"{message.author.mention} suggested for item {message.content}: {texture_url}"
    )
    return True


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if (
        await client.fetch_user(1191521256722399272) == message.author
    ):  # buildly is banned
        return

    if message.attachments:
        if message.channel.id == int(request_option("suggestions_channel")):
            if await validate_suggestion(message):
                if await send_png(message):
                    if len(get_jsons(message)) == 1:
                        print("this will activate the included json function, and do some weird stuff with blockbench models")
                        raise NotImplementedError
                    if len(get_jsons(message)) == 0:
                        print("this will activate the normal json function")
                        raise NotImplementedError

    if message.content.startswith("!setsuggest"):
        if await staff_checker(message):
            if len(message.channel_mentions) != 0:
                set_suggest_channel(message.channel_mentions[0].id)
            else:
                await message.channel.send("Please mention a channel")

    if message.content.startswith("!setstaff"):
        if await staff_checker(message):
            if len(message.channel_mentions) != 0:
                set_staff_channel(message.channel_mentions[0].id)
            else:
                await message.channel.send("Please mention a channel")

    if message.content.startswith("!getstaff"):
        stf_channel = request_option("staff_channel")
        await message.channel.send(f"<#{stf_channel}>")

    if message.content.startswith("!getsuggest"):
        sgst_channel = request_option("suggestions_channel")
        await message.channel.send(f"<#{sgst_channel}>")

    if message.content.startswith("!addstaff"):
        if await staff_checker(message):
            if len(message.role_mentions) != 0:
                add_staff(message.role_mentions[0].id)
            else:
                await message.channel.send("Please mention a user")

    if message.content.startswith("!removestaff"):
        if await staff_checker(message):
            if len(message.role_mentions) != 0:
                remove_staff(message.role_mentions[0].id)
            else:
                await message.channel.send("Please mention a user")

    if message.content.startswith("!requestitems"):
        await message.author.create_dm()
        items: list = gather_mc_items()
        first_quart = items[: len(items) // 4]
        second_quart = items[len(items) // 4 : len(items) // 2]
        third_quart = items[len(items) // 2 : 3 * len(items) // 4]
        fourth_quart = items[3 * len(items) // 4 :]
        await message.author.dm_channel.send(first_quart)
        await message.author.dm_channel.send(second_quart)
        await message.author.dm_channel.send(third_quart)
        await message.author.dm_channel.send(fourth_quart)


async def approved(payload: discord.RawReactionActionEvent):
    channel: discord.channel = client.get_channel(payload.channel_id)
    message: discord.Message = await channel.fetch_message(payload.message_id)
    approved_emoji = "👍"
    denied_emoji = "👎"

    if await staff_checker(message):
        if approved_emoji in [reaction.emoji for reaction in message.reactions]:
            await message.reply(f"Suggestion approved by <@{payload.user_id}>!")
            return True

        if denied_emoji in [reaction.emoji for reaction in message.reactions]:
            await message.reply(f"Suggestion denied by <@{payload.user_id}>!")
            return False
    if not await staff_checker(message):
        await message.channel.send("you are not authorized to approve")
        return


@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if payload.member.bot:
        return

    channel: discord.channel = client.get_channel(payload.channel_id)
    message: discord.Message = await channel.fetch_message(payload.message_id)
    user: discord.user = await client.fetch_user(payload.user_id)

    if await approved(payload):
        raise NotImplementedError


@client.event
async def on_ready():
    print(f"{client.user} im in")


client.run(TOKEN)
