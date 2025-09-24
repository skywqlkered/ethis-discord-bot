from dotenv import load_dotenv
import discord
import os
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_raw_audit_log_entry(payload):
    guild = discord.utils.get(client.guilds, id=payload.guild_id)
    channel = [channel for channel in guild.text_channels if channel.id == 1419086464985075723][0]
    channel.send('Hello {}'.format(payload.user))

client.run(TOKEN)