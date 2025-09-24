import discord
from discord.ext import commands
from functions.validation import gather_mc_items
import functions.channel_functions


class Texture(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__.split('.')[-1]} cog loaded.")

    @discord.slash_command(description="Add a texture to the resourcepack.")
    async def add_texture(self, ctx: discord.ApplicationContext, item_name: str = discord.Option(str, description="The name of the item you want to add.")):
        channel = await functions.channel_functions.create_channel(ctx, item_name)
        await ctx.respond(f"Created a channel at <#{channel.id}>", ephemeral=True)

    async def get_mc_items(ctx: discord.AutocompleteContext):
        """
        Autocomplete function to get Minecraft items based on user input.

        Args:
            ctx (discord.AutocompleteContext): The context of the autocomplete interaction.

        Returns:
            list: A list of up to 25 Minecraft items that match the user input.
        """
        user_input = ctx.value.lower()
        items = gather_mc_items()
        filtered_items = [item for item in items if user_input in item.lower()]
        return filtered_items[:25]

    @discord.slash_command(description="Select a Minecraft item.")
    async def select_item(
        self,
        ctx: discord.ApplicationContext,
        item: str = discord.Option(
            str, autocomplete=discord.utils.basic_autocomplete(get_mc_items), description="The Minecraft item you want to select."
        ),
    ):
        await ctx.respond(f"You selected the Minecraft item: `{item}`!")
        await ctx.channel.send(f"Send your image here to add it to the resourcepack, make your texture is a `png`, has `rgb colormode` and the `dimensions are a power of 2`. React to your image with ✅ to confirm it.") 

        return item


def setup(bot):
    bot.add_cog(Texture(bot))
