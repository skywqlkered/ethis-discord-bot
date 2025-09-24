from dotenv import load_dotenv
import discord
import os
import asyncio

load_dotenv()
TOKEN = os.getenv('ETHIS_BOT_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))




welcome_message = """
Then a <@&1261617495954034698> member will process your ticket shortly!

```
**What do you enjoy doing in Minecraft?**
- Answer

**What has been your experience playing on Minecraft servers or SMPs?**
- Answer

**Tell us more about yourself! Share your hobbies, a fun fact, or anything else you’d like us to know!**
- Answer


``` 


"""


def setup_embed() -> discord.Embed:
    embed: discord.Embed = discord.Embed(color=discord.Color.from_rgb(216, 107, 44))
    embed.add_field(name='Please answer the questions below:', value=welcome_message, inline=True)
    return embed


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if message.content.startswith('/send form') and 1261617495954034698 in [role.id for role in message.author.roles]:
        try:
            await message.channel.send(embed=setup_embed())
            await message.delete()
        except Exception as errorman:
            await message.guild.get_channel(1419741195424366612).send(str(errorman))

#     if message.author.id == 398769543482179585 and message.content.startswith('/sort channels'):
#
#         applog1 = message.guild.get_channel(926090262185377812)
#         applog2 = message.guild.get_channel(1203382161936486480)
#         applog3 = message.guild.get_channel(1226168255983652894)
#         applog4 = message.guild.get_channel(1226215932704325702)
#
#         applog5: discord.CategoryChannel = message.guild.get_channel(1294969300725141655)
#         staffapp: discord.CategoryChannel = message.guild.get_channel(1420506502506090516)
#
#         whitelist: discord.CategoryChannel = message.guild.get_channel(1420508979318096006)
#         whitelistp2: discord.CategoryChannel = message.guild.get_channel(1420534780658974720)
#         whitelistp3: discord.CategoryChannel = message.guild.get_channel(1420537439012913323)
#         ticket: discord.CategoryChannel = message.guild.get_channel(1420509042367004752)
#
#         whitelists2: discord.CategoryChannel = message.guild.get_channel(1420525392145416302)
#         tickets2: discord.CategoryChannel = message.guild.get_channel(1420530121936343160)
#
#
#         # stringe = "closed-0042"
#         # number = stringe.split("-")[1]
#
#         for channel in applog1.text_channels:
#             channel: discord.TextChannel
#
#             first_message_list: list[discord.Message] = await channel.history(limit=1, oldest_first=True).flatten()
#             first_message: discord.Message = first_message_list[0]
#             first_message.mentions[0].name

#             year, month, day = str(first_message.created_at).split(' ')[0].split('-')
#             month = int(month)
#             year = int(year)
#
#
#             await asyncio.sleep(0.5)
#             ticket_number = first_message.channel.name.split("-")[-1]
#             try:
#                 if len(first_message.embeds) == 2 and "**Which role are you applying for?**" in first_message.embeds[1].description: # staff
#                     await channel.move(end=True,category=staffapp)
#                     await channel.edit(name=(first_message.mentions[0].name + "-" + ticket_number))
#                     continue
#
#                 if len(first_message.embeds) == 2 and "**Which role are you applying for?**" not in first_message.embeds[1].description or int(ticket_number) < 30: # whitelist
#                     await channel.edit(name=(first_message.mentions[0].name + "-" + ticket_number))
#
#                     if (month < 8 and year == 2024) or year < 2024: # season1
#                         await channel.move(end=True, category=whitelistp3)
#                     if (month >= 8 and year >= 2024) or year == 2025: # season2
#                         await channel.move(end=True, category=whitelists2)
#                     continue
#
#                 if len(first_message.embeds) == 1 and int(ticket_number) > 29: # support
#                     await channel.edit(name=(first_message.mentions[0].name + "-" + ticket_number))
#                     if (month < 8 and year == 2024) or year < 2024: # season1
#                         await channel.move(end=True, category=ticket)
#                     if (month >= 8 and year >= 2024) or year == 2025: # seaosn2
#                         await channel.move(end=True, category=tickets2)
#                     continue
#
#             except discord.HTTPException:
#                 continue
#         print("done sorting")
#
#     if message.author.id == 398769543482179585 and message.content.startswith('/reverse'):
#         applog5: discord.CategoryChannel = message.guild.get_channel(1294969300725141655)
#
#         staffapp: discord.CategoryChannel = message.guild.get_channel(1420506502506090516)
#         whitelist: discord.CategoryChannel = message.guild.get_channel(1420508979318096006)
#         ticket: discord.CategoryChannel = message.guild.get_channel(1420509042367004752)
#
#         for cat in [staffapp, whitelist, ticket]:
#             for channel in cat.text_channels:
#                 await asyncio.sleep(0.5)
#                 await channel.move(end=True, category=applog5)
# #
#         print("done reversing")
@client.event
async def on_guild_channel_create(channel: discord.abc.GuildChannel):
    if channel.category is None:
        return
    if channel.category.id == 1226215408126791832 and channel.name.startswith('ticket'):
        try:
            def check(message):
                return message.channel == channel

            await client.wait_for('message', check=check)
            await channel.send(embed=setup_embed())
        except Exception as errorman:
            await channel.guild.get_channel(1419741195424366612).send(str(errorman))

@client.event
async def on_guild_channel_update(before, after):
    if isinstance(after, discord.TextChannel):
        after: discord.TextChannel
        if after.name.startswith('closed'):
            try:
                first_message_list: list[discord.Message] = await after.history(limit=1, oldest_first=True).flatten()
                first_message: discord.Message = first_message_list[0]
                await after.edit(name=(first_message.mentions[0].name + "-" + first_message.channel.name.split("-")[-1]))
            except Exception as errorman:
                await after.guild.get_channel(1419741195424366612).send(str(errorman))

client.run(TOKEN)
