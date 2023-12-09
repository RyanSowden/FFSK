import discord 
import os
from discord.ext import commands
from discord import app_commands
from sleeper_wrapper import League
import pandas as pd
from tabulate import tabulate
from db_connect import connection
import re
import os

GUILD = os.getenv('GUILD_ID')
c = connection.cursor()



class Matchups(commands.Cog):

    def __init__(self,bot:commands.Bot) -> None:
        self.bot = bot


    @app_commands.command(name='matchups')
    async def get_matchups(self,interaction: discord.Interaction, league: str, week:str) -> None:
        """League matchups and points"""
        try:
            c.execute("SELECT league_number FROM league WHERE league_name = %s;",(league,))
            rows = c.fetchall()
            if not rows: #if none found, return error
                await interaction.response.send_message('No league found.')
            else:
                self.results = str(re.sub(r"[]),[('']", '', str(rows))) #stripping results of query so it can be passed to the table
                self.league = League(self.results)
                self.week = week
                self.league_name = self.league.get_league()
                self.rosters = self.league.get_rosters()
                self.users = self.league.get_users()
                self.matchups = self.league.get_matchups(self.week)
                self.scoreboards = self.league.get_scoreboards(self.rosters,self.matchups,self.users,self.week)
                self.df = pd.DataFrame.from_dict(self.scoreboards)
                # Get the number of columns dynamically
                num_columns = len(self.df.columns)
                if num_columns == 0:
                    await interaction.response.send_message('No data found.')

                else:
                    self.embed = discord.Embed()
                    # Create a list to store table data
                    table_data_list = []


                # Create tables dynamically
                    for i in range(1, num_columns + 1):
                        table_data = "```" + tabulate(self.df[i], headers=[], showindex=False, tablefmt='plain') + "```"
                        table_data_list.append(str(re.sub(r"[),[('']", '', str(table_data))))
                    
             # Create fields dynamically
                    for i in range(1, num_columns + 1):
                        self.embed.add_field(name=str(i), value=table_data_list[i - 1], inline=False)

                    self.embed.title = f"{self.league_name['name']} Matchups Week {self.week}"
                    self.embed.colour = 15548997

                    await interaction.response.defer()
                    await interaction.followup.send(embed=self.embed)



        except Exception as e:
            self.embed = discord.Embed()
            # If there is a ValueError (arrays with different lengths), embed the raw data
            self.embed.title = f"{self.league_name['name']} Matchups Week {self.week}"

            # Concatenate all arrays into one table, removing symbols but keeping decimal points and letters
            raw_scoreboard_str = "\n".join([re.sub(r'[^\d.a-zA-Z\s]', '', tabulate({key: value}, tablefmt='plain')) for key, value in self.scoreboards.items()])
            self.embed.add_field(name="", value=f"```{raw_scoreboard_str}```", inline=False)
            self.embed.colour = 15548997

            await interaction.response.defer()
            await interaction.followup.send(embed=self.embed)

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Matchups(bot), guilds=[discord.Object(id=GUILD)])