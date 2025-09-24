import discord
from discord.ext import commands
from functions import admin
from discord import Option


class Staff(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__.split('.')[-1]} cog loaded.")

    class MyView(discord.ui.View):
        @staticmethod
        def get_options():
            options = []  # Initialize an empty list to store the options
            for i in admin.get_staff_roles():
                options.append(discord.SelectOption(label=f"{i[1]}"))
            return options

        @discord.ui.select(
            placeholder="Choose a Role",
            min_values=1,
            max_values=1,
            options=get_options()
        )
        async def select_callback(self, select, interaction):
            admin.remove_staff(select.values[0])
            await interaction.response.send_message(f"You removed <@&{select.values[0]}> from the staff roles.", ephemeral=True)

    @discord.slash_command(description="Remove a role as staff (press enter to open the select menu).")
    async def remove_staff(self, ctx: discord.ApplicationContext):
        await ctx.respond("Choose a role to remove from the staff roles.", view=Staff.MyView(), ephemeral=True)

    @discord.slash_command(description="Add a role as staff.")
    async def set_staff_role(
        self,
        ctx: discord.ApplicationContext,
        role: discord.Role = discord.Option(
            discord.Role,
            name="role",
            description="What role are you assigning?"
        ),

    ):
        admin.add_staff(role.id, role.name)
        await ctx.respond(f"You added the role `{role}` to the staff roles.", ephemeral=True)

    @discord.slash_command(description="Set the category for the texture channels.")
    async def set_category(self,
                           ctx: discord.ApplicationContext,
                           category: discord.CategoryChannel = discord.Option(discord.CategoryChannel,
                                                                              name="category",
                                                                              description="What category are you assigning?")):
        if await admin.perm_check(ctx.author, ctx):
            admin.set_texture_category(category)
            await ctx.respond(f"Set the category to {category.name}", ephemeral=True)

        else:
            await ctx.respond("You do not have the permissions to use this command.", ephemeral=True)


def setup(bot):
    bot.add_cog(Staff(bot))
