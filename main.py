import os
import shutil
import discord
from dotenv import load_dotenv
from discord.ext import tasks
from discord import app_commands
from functions.admin import *
from functions.validation import *
from functions.json_functions import *
from functions.dropbox_functions import *


# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


# Helper functions as they were in your original code
async def get_previous(message: discord.Message):
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
    if not await download_attach(attach, content[1], True):
        await message.channel.send("This model already exists")
        return
    edit_or_create(
        parent="generated", placeholder_model=content[1], placeholder_texture=content[0]
    )


async def john(message: discord.Message):
    jsonattach = get_jsons(message)[0]
    pngattach = get_pngs(message)[0]
    content = await get_content(message)
    if not await download_attach(jsonattach, content[0], False):
        await message.channel.send("This model already exists")
        return
    if not await download_attach(pngattach, content[1], True):
        await message.channel.send("This model already exists")
        return


# # Slash Command Definitions
# @tree.command(name="refresh", description="Refresh Dropbox content")
# async def refresh(interaction: discord.Interaction):
#     upload_dropbox()
#     await interaction.response.send_message("Refreshed Dropbox!")


# @tree.command(name="setsuggest", description="Set the suggestion channel")
# async def setsuggest(interaction: discord.Interaction, channel: discord.TextChannel):
#     if await perm_check(interaction.user, interaction):
#         set_suggest_channel(channel.id)
#         await interaction.response.send_message(
#             f"Set suggestion channel to {channel.mention}"
#         )
#     else:
#         await interaction.response.send_message("You don't have permission to do that.")


# @tree.command(name="send", description="Send server pack")
# async def send(interaction: discord.Interaction):
#     src = r"C:\Users\Julian\Documents\Github\ethis-discord-bot\server_pack"
#     dest = r"C:\Users\Julian\curseforge\minecraft\Instances\fabric 1.20.2\resourcepacks"

#     if interaction.user.id == 398769543482179585:
#         if not os.path.exists(src):
#             await interaction.response.send_message("Source path does not exist.")
#             return

#         dest_path = os.path.join(dest, "server_pack")
#         try:
#             if os.path.exists(dest_path):
#                 shutil.rmtree(dest_path)
#             shutil.copytree(src, dest_path)
#             await interaction.response.send_message("Server pack copied successfully.")
#         except Exception as e:
#             await interaction.response.send_message(
#                 f"Failed to copy server pack: {str(e)}"
#             )
#     else:
#         await interaction.response.send_message("no you dont lil monke.")
#         interaction.user.roles


# @tree.command(name="setstaff", description="Set the staff channel")
# async def setstaff(interaction: discord.Interaction, channel: discord.TextChannel):
#     if await perm_check(interaction.user, interaction):
#         set_staff_channel(channel.id)
#         await interaction.response.send_message(
#             f"Set staff channel to {channel.mention}"
#         )
#     else:
#         await interaction.response.send_message("You don't have permission to do that.")


# @tree.command(name="getstaff", description="Get the staff channel")
# async def getstaff(interaction: discord.Interaction):
#     stf_channel = request_option("staff_channel")
#     await interaction.response.send_message(f"<#{stf_channel}>")


# @tree.command(name="getsuggest", description="Get the suggestion channel")
# async def getsuggest(interaction: discord.Interaction):
#     sgst_channel = request_option("suggestions_channel")
#     await interaction.response.send_message(f"<#{sgst_channel}>")


# @tree.command(name="addstaff", description="Add a role to staff")
# async def addstaff(interaction: discord.Interaction, role: discord.Role):
#     if await perm_check(interaction.user, interaction):
#         add_staff(role.id)
#         await interaction.response.send_message(f"Added {role.mention} to staff")
#     else:
#         await interaction.response.send_message("You don't have permission to do that.")


# @tree.command(name="removestaff", description="Remove a role from staff")
# async def removestaff(interaction: discord.Interaction, role: discord.Role):
#     if await perm_check(interaction.user, interaction):
#         remove_staff(role.id)
#         await interaction.response.send_message(f"Removed {role.mention} from staff")
#     else:
#         await interaction.response.send_message("You don't have permission to do that.")


# @tree.command(name="requestitems", description="Request Minecraft items")
# async def requestitems(interaction: discord.Interaction):
#     await interaction.user.create_dm()
#     items = gather_mc_items()
#     first_quart = items[: len(items) // 4]
#     second_quart = items[len(items) // 4 : len(items) // 2]
#     third_quart = items[len(items) // 2 : 3 * len(items) // 4]
#     fourth_quart = items[3 * len(items) // 4 :]

#     await interaction.user.dm_channel.send(first_quart)
#     await interaction.user.dm_channel.send(second_quart)
#     await interaction.user.dm_channel.send(third_quart)
#     await interaction.user.dm_channel.send(fourth_quart)

#     await interaction.response.send_message("Sent items to your DM!")


@tree.command(name="list", description="List all the current online players")
async def list(interaction: discord.Interaction):
    await interaction.response.send_message(get_online_players(), ephemeral=True)


# Event listeners and task scheduling
@client.event
async def on_ready():
    GUILD_ID = discord.Object(id=987779478413525023)
    await tree.sync(guild=GUILD_ID)
    print(f"{client.user} is ready!")


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if (
        await client.fetch_user(1191521256722399272) == message.author
    ):  # buildly is banned
        return

    if message.channel.id == int(request_option("suggestions_channel")):
        if message.attachments:
            if await validate_suggestion(message):
                if len(get_jsons(message)) == 1:
                    await john(message)
                if len(get_jsons(message)) == 0:
                    await no_john(message)
                await send_png(message)


# async def approved(payload: discord.RawReactionActionEvent):
#     channel: discord.channel = client.get_channel(payload.channel_id)
#     approver = await client.fetch_user(payload.user_id)
#     message: discord.Message = await channel.fetch_message(payload.message_id)
#     approved_emoji = "👍"
#     denied_emoji = "👎"

#     if await perm_check(approver, message):
#         if approved_emoji in [reaction.emoji for reaction in message.reactions]:
#             await message.reply(f"Suggestion approved by <@{payload.user_id}>!")
#             return True

#         if denied_emoji in [reaction.emoji for reaction in message.reactions]:
#             await message.reply(f"Suggestion denied by <@{payload.user_id}>!")
#             return False
#     if not await perm_check(approver, message):
#         await message.channel.send("you are not authorized to approve")
#         return


# @client.event
# async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
#     if payload.member.bot:
#         return

#     channel: discord.TextChannel = client.get_channel(payload.channel_id)
#     message: discord.Message = await channel.fetch_message(payload.message_id)
#     user: discord.User = await client.fetch_user(payload.user_id)

#     if await approved(payload):
#         raise NotImplementedError


@tasks.loop(seconds=3600.0)
async def update_pack():
    upload_dropbox()


# Start the bot
client.run(TOKEN)
