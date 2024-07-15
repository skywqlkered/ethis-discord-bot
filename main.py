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
        print(message.attachments[0].url)
        
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
        config: configparser.ConfigParser = gather_configini()
        return config.get("CHANNEL", config_option)

    def set_suggest_channel(id: int):
        config: configparser.ConfigParser = gather_configini()
        config.set("CHANNEL", "suggestions_channel", str(id))
        with open("config.ini", "w") as configfile:
            config.write(configfile)

    def set_staff_channel(id: int):
        config = gather_configini()
        config.set("CHANNEL", "staff_channel", str(id))
        with open("config.ini", "w") as configfile:
            config.write(configfile)

    def add_staff(id: int):
        config = gather_configini()
        # add new adiiotns rather than replace
        config.read("config.ini")
        staff_str = config.get("CHANNEL", "staff_roles") + "," + str(id)
        config.set("CHANNEL", "staff_roles", staff_str)
        print ("staff added")
        with open("config.ini", "w") as configfile:
            config.write(configfile)

    def remove_staff(id: int):
        config = gather_configini()
        # add new adiiotns rather than replace
        config.read("config.ini")
        staff_str = config.get("CHANNEL", "staff_roles")
        rem_staff = staff_str.replace(str(id), "")
        if rem_staff.startswith(","):
            rem_staff = rem_staff[1:]
        if rem_staff.endswith(","):
            rem_staff = rem_staff[:-1]
        config.set("CHANNEL", "staff_roles", rem_staff)
        print ("staff removed")
        
        with open("config.ini", "w") as configfile:
            config.write(configfile)

    async def check_if_owner(Message: discord.Message) -> bool:
        if Message.author.id == Message.guild.owner_id:

            return True

        else:  
            return False
    

    async def check_if_staff(user: discord.user, message: discord.Message) -> bool:
        roles = (await message.guild.fetch_member(user.id)).roles
        config = gather_configini()
        staff_list = (config.get("CHANNEL", "staff_roles")).split(",")
        for role in roles:
            if str(role.id) in staff_list:
                return True

        return False

    async def checker(message):
        return await check_if_owner(message) or await check_if_staff(message.author, message)


    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if await client.fetch_user(1191521256722399272) == message.author:
            return

        await message.channel.send("monke0")
        if message.attachments:
            await message.channel.send("monke1")

            if message.channel.id == request_option("suggestions_channel"):
                await message.channel.send("monke2")
                await get_png(message)

        if message.content.startswith("!setsuggest"):
            if await checker(message):
                if len(message.channel_mentions) != 0:
                    set_suggest_channel(message.channel_mentions[0].id)
                else:
                    await message.channel.send("Please mention a channel")

        if message.content.startswith("!setstaff"):
            if await checker(message):
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
            if await checker(message):
                if len(message.role_mentions) != 0:
                    add_staff(message.role_mentions[0].id)
                else:
                    await message.channel.send("Please mention a user")

        if message.content.startswith("!removestaff"):
            if await checker(message):
                if len(message.role_mentions) != 0:
                    remove_staff(message.role_mentions[0].id)
                else:
                    await message.channel.send("Please mention a user")

        if message.content.startswith("!test"):
            await message.channel.send(await check_if_owner(message))


    def get_img_for_message(Message):
        raise NotImplementedError

    @client.event
    async def on_ready():
        print(f"{client.user} im in")

    client.run(TOKEN)


run_bot()

