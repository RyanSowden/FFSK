import discord 
import os
from discord import app_commands
from discord.ext import commands
from tabulate import tabulate


GUILD = os.getenv('GUILD_ID')

class Help(commands.Cog):

    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot


    @app_commands.command(name='help')
    async def get_help(self, interaction: discord.Interaction) -> None:
        """Gets all available commands"""   
        self.embed = discord.Embed(title='Command List', colour=5793266)
        self.embed.add_field(name='assign', value='Assign a team name to a league id,takes 2 arguments(league,#)(*must have sufficient role).', inline=False)
        self.embed.add_field(name='reassign', value='Reassign a team name ot a new League ID, takes 2 arguments(league,#)(*must have sufficient role).', inline=False)
        self.embed.add_field(name='lineups', value='Gets the current starting lineups for given league, takes 2 arguments(league,week)', inline=False)
        self.embed.add_field(name='matchups', value='Gets the current matchups for given league, takes 2 arguments(league,week)', inline=False)
        self.embed.add_field(name='standings', value='Gets the current standings for given league, takes 1 argument(league)', inline=False)

        await interaction.response.send_message(embed=self.embed)

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Help(bot), guilds=[discord.Object(id=GUILD)])

