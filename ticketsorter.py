from dotenv import load_dotenv
import discord
import os
import asyncio

load_dotenv()
TOKEN = os.getenv('BRENS_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

client.run(TOKEN)