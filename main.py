"""
using pycord as discord api
"""

import discord
from dotenv import load_dotenv
import os
import functions.channel_functions

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


intents = discord.Intents.all()
bot = discord.Bot(intents=intents)


# this decorator makes a slash command
@bot.command(description="Sends the bot's latency.")
async def ping(ctx):  # a slash command will be created with the name "ping"
    await ctx.respond(f"Pong! Latency is {bot.latency}")


@bot.event
async def on_connect():
    if bot.auto_sync_commands:
        await bot.sync_commands()
    print(f"{bot.user.name}, im in.")


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    if message.author == await bot.fetch_user(398769543482179585) and message.content.startswith("!sync"):
        print("testo commando")
        await bot.sync_commands(guild_ids=[987779478413525023])
        await message.reply("Synced commands.")

    if message.content.startswith("!create"):
        pass
    if message.content.startswith("!cleararchiv") and message.author.id == 398769543482179585:
        for cat in message.guild.categories:
            if cat.name == "archiv":
                archiv = cat
        for channel in archiv.channels:
            await channel.delete()


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    channel: discord.TextChannel = bot.get_channel(payload.channel_id)
    if channel.category.name == "texture-adder" and payload.emoji.name == "❌" and payload.user_id != bot.user.id:
        await channel.edit(category=functions.channel_functions.archiv, sync_permissions=True, position=1)
    if channel.category.name == "texture-adder" and payload.emoji.name == "✅" and payload.user_id != bot.user.id and bot.get_message(payload.message_id).attachments.__len__() > 0:
        raise NotImplementedError("Not implemented yet.")


def load_cogs():
    for filename in os.listdir("commands"):
        if filename.endswith(".py"):
            bot.load_extension(f"commands.{filename[:-3]}")


load_cogs()
bot.run(TOKEN)
