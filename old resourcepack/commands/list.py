import discord
from discord.ext import commands
from functions.admin import get_online_players

class List(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__.split('.')[-1]} cog loaded.")


    @discord.slash_command(description="List of online players")
    async def list(self, ctx: discord.ApplicationContext):
        await ctx.response.send_message(get_online_players(), ephemeral=True)
    
def setup(bot):
    bot.add_cog(List(bot))