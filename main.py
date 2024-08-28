import os
import shutil

import discord
from dotenv import load_dotenv
import configparser
import dropbox
from discord.ext import tasks


from functions.admin import *
from functions.validation import *
from functions.json_functions import *
from functions.dropbox_functions import *

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
client = discord.Client(intents=intents)


async def get_previous(message: discord.message):
    previous_msg = None
    staff_channel: discord.channel = await client.fetch_channel(
        int(request_option("staff_channel"))
    )
    async for msg in staff_channel.history(limit=1):
        previous_msg = msg
        break
    return previous_msg


async def get_png(message: discord.Message):
    png: discord.Attachment = get_pngs(message)[0]
    texture_url: str = png.url.split("?ex")[0]
    return texture_url


async def send_png(message: discord.Message) -> bool:

    await message.reply("Suggested!")

    url = await get_png(message)
    staff_channel: discord.channel = await client.fetch_channel(
        int(request_option("staff_channel"))
    )

    content = await get_content(message)
    await staff_channel.send(
        f"{message.author.mention} suggested for item **{content[0]}**: {url}"
    )
    return True


async def no_john(message: discord.Message):
    attach = get_pngs(message)[0]
    content = await get_content(message)
    if not await download_attach(attach, content[1]):
        await message.channel.send("This model already exists")
        return

    edit_or_create(
        parent="generated", placeholder_model=content[1], placeholder_texture=content[0]
    )


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
                if len(get_jsons(message)) == 1:
                    print(
                        "this will activate the included json function, and do some weird stuff with blockbench models"
                    )
                    raise NotImplementedError
                if len(get_jsons(message)) == 0:
                    await no_john(message)

                await send_png(message)
            

    if message.content.startswith("!setsuggest"):
        if await perm_check(message.author, message):
            if len(message.channel_mentions) != 0:
                set_suggest_channel(message.channel_mentions[0].id)
                await message.channel.send (f"Set suggestion channel to <#{message.channel_mentions[0].id}>")
            else:
                await message.channel.send("Please mention a channel")

    if message.content.startswith("!send"):
        src = r"C:\Users\Julian\Documents\Github\ethis-discord-bot\server_pack"
        dest = r"C:\Users\Julian\curseforge\minecraft\Instances\fabric 1.20.2\resourcepacks"

        # Check if the source directory exists
        if not os.path.exists(src):
            return False

        # Define the destination directory
        dest_path = os.path.join(dest, "server_pack")

        # Copy the server_pack directory
        try:
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)  # Remove the existing directory
            shutil.copytree(src, dest_path)
            return True
        except Exception as e:
            return False

    if message.content.startswith("!setstaff"):
        if await perm_check(message.author, message):
            if len(message.channel_mentions) != 0:
                set_staff_channel(message.channel_mentions[0].id)
                await message.channel.send (f"Set staff channel to <#{message.channel_mentions[0].id}>")

            else:
                await message.channel.send("Please mention a channel")

    if message.content.startswith("!getstaff"):
        stf_channel = request_option("staff_channel")
        await message.channel.send(f"<#{stf_channel}>")

    if message.content.startswith("!getsuggest"):
        sgst_channel = request_option("suggestions_channel")
        await message.channel.send(f"<#{sgst_channel}>")

    if message.content.startswith("!addstaff"):
        if await perm_check(message.author, message):
            if len(message.role_mentions) != 0:
                add_staff(message.role_mentions[0].id)
                await message.channel.send (f"Added {message.role_mentions[0]} to staff")

            else:
                await message.channel.send("Please mention a user")

    if message.content.startswith("!removestaff"):
        if await perm_check(message.author,message):
            if len(message.role_mentions) != 0:
                remove_staff(message.role_mentions[0].id)
                await message.channel.send (f"Removed {message.role_mentions[0]} from staff")
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
    approver = await client.fetch_user(payload.user_id)
    message: discord.Message = await channel.fetch_message(payload.message_id)
    approved_emoji = "👍"
    denied_emoji = "👎"

    if await perm_check(approver, message):
        if approved_emoji in [reaction.emoji for reaction in message.reactions]:
            await message.reply(f"Suggestion approved by <@{payload.user_id}>!")
            return True

        if denied_emoji in [reaction.emoji for reaction in message.reactions]:
            await message.reply(f"Suggestion denied by <@{payload.user_id}>!")
            return False
    if not await perm_check(approver, message):
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


@tasks.loop(seconds=3600.0)
async def update_pack():
    upload_dropbox()

@client.event
async def on_ready():
    print(f"{client.user} im in")
    update_pack.start()


client.run(TOKEN)
