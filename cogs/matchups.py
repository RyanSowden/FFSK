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



class Matchups(commands.Cog):

    def __init__(self,bot:commands.Bot) -> None:
        self.bot = bot


    @app_commands.command(name='matchups')
    async def get_matchups(self,interaction: discord.Interaction, league: str, week:str) -> None:
        """League matchups and points"""
        try:
            c.execute("SELECT league_number FROM league WHERE league_name = %s;",(league,))
            rows = c.fetchall()
            if len(rows) == 0: #if none found, return error
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
                self.df[self.df.columns[[0,1,2,3]]]
                self.transpose_df = self.df.transpose()
                
                '''
                 To make sure the matchups display correctly inside discord, each table result needs to be returned as an individual result and made into a seperate table
                 '''
                self.table_data1 = "```" +  tabulate(self.df[1], headers=[], showindex=False, tablefmt='plain')+ "```"
                self.table_data2 = "```" +  tabulate(self.df[2], headers=[], showindex=False, tablefmt='plain')+ "```"
                self.table_data3 = "```" +  tabulate(self.df[3], headers=[], showindex=False, tablefmt='plain')+ "```"
                self.table_data4 = "```" +  tabulate(self.df[4], headers=[], showindex=False, tablefmt='plain')+ "```"
                self.table_data5 = "```" +  tabulate(self.df[5], headers=[], showindex=False, tablefmt='plain')+ "```"
                self.table_data6 = "```" +  tabulate(self.df[6], headers=[], showindex=False, tablefmt='plain')+ "```"
                self.table1 = str(re.sub(r"[),[('']", '', str(self.table_data1)))
                self.table2 = str(re.sub(r"[),[('']", '', str(self.table_data2)))
                self.table3 = str(re.sub(r"[),[('']", '', str(self.table_data3)))
                self.table4 = str(re.sub(r"[),[('']", '', str(self.table_data4)))
                self.table5 = str(re.sub(r"[),[('']", '', str(self.table_data5)))
                self.table6 = str(re.sub(r"[),[('']", '', str(self.table_data6)))
                self.embed = discord.Embed(title=self.league_name['name'] + ' ' + 'Matchups' + ' ' + 'Week' + ' ' + self.week, colour=15548997)
                self.embed.add_field(name='1', value=self.table1, inline=False)
                self.embed.add_field(name='2', value=self.table2, inline=False)
                self.embed.add_field(name='3', value=self.table3, inline=False)
                self.embed.add_field(name='4', value=self.table4, inline=False)
                self.embed.add_field(name='5', value=self.table5, inline=False)
                self.embed.add_field(name='6', value=self.table6, inline=False)
                await interaction.response.defer()
                await interaction.followup.send(embed=self.embed)

        except Exception as e:
            connection.rollback()
            print(e)
            await interaction.response.send_message("Whoops, something went wrong")

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Matchups(bot), guilds=[discord.Object(id=GUILD)])