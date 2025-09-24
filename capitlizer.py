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
    if message.author.id == 854717416688451604:
        await message.channel.send(f"{message.content[0].upper()}{message.content[1:].lower()}.")
        await message.delete()

client.run(TOKEN)