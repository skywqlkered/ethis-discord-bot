import discord
from discord.ext import commands


class TestCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Test command cog loaded.")

    @discord.slash_command()
    async def test(self, ctx: discord.ApplicationContext):
        await ctx.respond("yo", ephemeral=True)
        

def setup(bot):
    bot.add_cog(TestCommand(bot))