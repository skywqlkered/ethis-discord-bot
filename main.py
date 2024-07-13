import discord
from discord import app_commands
import os
from dotenv import load_dotenv
import json
import configparser

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


def run_bot():
    async def get_png(message):
        # check if message attch is a png
        texture_url = message.attachments[0].url.split("?ex")[0]
        print(texture_url)
        if texture_url.endswith(".png"):
            await message.channel.send(texture_url)
            await message.channel.send("WAAAAAAAAAA")
        else:
            await message.channel.send("File must be png")

    def gather_configini():
        config = configparser.ConfigParser()
        config.read("config.ini")
        return config

    def request_option(config_option: str):
        config = gather_configini()
        return config.get("CHANNEL", config_option)

    def set_suggest_channel(id: int):
        config = gather_configini()
        config.set("CHANNEL", "suggestions_channel", str(id))
        with open("config.ini", "w") as configfile:
            config.write(configfile)

    def set_staff_channel(id: int):
        config = gather_configini()
        config.set("CHANNEL", "staff_channel", str(id))
        with open("config.ini", "w") as configfile:
            config.write(configfile)

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if await client.fetch_user(1191521256722399272) == message.author:
            return

        if message.attachments:
            if message.channel.id == request_option("suggestions_channel"):
                await get_png(message)

        if message.content.startswith("!suggest"):
            if len(message.channel_mentions) != 0:
                set_suggest_channel(message.channel_mentions[0].id)
            else:
                await message.channel.send("Please mention a channel")

        if message.content.startswith("!staff"):
            if len(message.channel_mentions) != 0:
                set_staff_channel(message.channel_mentions[0].id)
            else:
                await message.channel.send("Please mention a channel")

        if message.content.startswith("!getstaff"):
            stf_channel = request_option("staff_channel")
            await message.channel.send(f"<#{stf_channel}>")
    def get_img_for_message(Message):
        raise NotImplementedError

    @client.event
    async def on_ready():
        print(f"{client.user} im in")

    client.run(TOKEN)


run_bot()
