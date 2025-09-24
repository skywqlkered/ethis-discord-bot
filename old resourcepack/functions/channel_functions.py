import discord
import asyncio
archiv = None


async def create_channel(message: discord.Message, givn_name):
    global archiv
    item_name = givn_name
    guildl = message.guild
    for i in guildl.categories:
        if i.name == "texture-adder":
            cathegorie = i
        if i.name == "archiv":
            archiv = i
    overwrites = {
            message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            message.guild.me: discord.PermissionOverwrite(read_messages=True),
            message.author: discord.PermissionOverwrite(read_messages=True), 
        }       
    channel = await guildl.create_text_channel(name=item_name, category=cathegorie, overwrites=overwrites)
    react_message = await channel.send(f"{message.author.mention}, react to this message to close the channel.")
    await react_message.add_reaction("❌")
    await channel.send("Use `/select_item` to select the Mincraft item.")
    return channel
