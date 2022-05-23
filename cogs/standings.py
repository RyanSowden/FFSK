import discord
import os 
from discord.ext import commands
from discord import app_commands
from sleeper_wrapper import League
import pandas as pd
from tabulate import tabulate
from db_connect import connection
import re

GUILD = os.getenv('GUILD_ID')
c = connection.cursor()

#bot command to get the standings for the requested league, will work for any sleeper league as logn as you have the league ID.

class Standings(commands.Cog):

    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot


    @app_commands.command(name='standings')
    async def get_standings(self, interaction: discord.Interaction, league: str):
        """League standings"""
        try:
            c.execute("SELECT league_number FROM league WHERE league_name = %s;",(league,))
            rows = c.fetchall()
            if len(rows) == 0: #if none found, return error
                await interaction.response.send_message('No league found.')
            else:
                self.results = str(re.sub(r"[]),[('']", '', str(rows))) #stripping results of query so it can be passed to the table
                self.league = League(self.results)
                self.league_name = self.league.get_league()
                self.rosters = self.league.get_rosters()
                self.users = self.league.get_users()
                self.standings = self.league.get_standings(self.rosters,self.users)
                self.df = pd.DataFrame.from_dict(self.standings) #returning the standings as a dataframe
                self.results = (self.df[self.df.columns[[0,1,2]]])#closing which columns to return
                self.results['W/L']=self.results[1] + '-'+ self.results[2]#adding the 'W/L' ratio
                self.table_data = self.results.drop([1,2], axis=1) #dropping the 2 W/L columns as they are no longer needed
                self.table = "```" + tabulate(self.table_data, headers=['Name','W/L'], showindex=False, tablefmt='plain') + "```" #formatting the table   
                self.embed = discord.Embed(title=self.league_name['name'] + ' ' + 'Standings', description=self.table, colour=15844367) #setting up the table to be embeded
                await interaction.response.defer()
                await interaction.followup.send(embed=self.embed)

        except Exception:
            connection.rollback()
            await interaction.response.send_message('Whoops something went wrong')

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Standings(bot), guilds=[discord.Object(id=GUILD)])