from email import message
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

#bot command to get the starting lineups for all palers in the requested league.
class Lineups(commands.Cog):

    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot


    @app_commands.command(name='lineups')
    async def get_lineups(self,interaction: discord.Interaction,league: str, week: str) -> None:
        """League starting lineups"""
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
                self.lineups = self.league.get_lineups(self.rosters,self.matchups,self.users,self.week)
                self.df = pd.DataFrame.from_dict(self.lineups)
                self.result = self.df.transpose()
            #Below fetches the usernames in the league, which is used for the table headings.'''
                self.p1 = self.result.loc[0,0]
                self.p2 = self.result.loc[1,0]
                self.p3 = self.result.loc[2,0]
                self.p4 = self.result.loc[3,0]
                self.p5 = self.result.loc[4,0]
                self.p6 = self.result.loc[5,0]
                self.p7 = self.result.loc[6,0]
                self.p8 = self.result.loc[7,0]
                self.p9 = self.result.loc[8,0]
                self.p10 = self.result.loc[9,0]
                self.p11 = self.result.loc[10,0]
                self.p12 = self.result.loc[11,0]
            #Below fetches the teams to be sent to the database'''
                self.t1 = self.result.loc[0,1]
                self.t2 = self.result.loc[1,1]
                self.t3 = self.result.loc[2,1]
                self.t4 = self.result.loc[3,1]
                self.t5 = self.result.loc[4,1]
                self.t6 = self.result.loc[5,1]
                self.t7 = self.result.loc[6,1]
                self.t8 = self.result.loc[7,1]
                self.t9 = self.result.loc[8,1]
                self.t10 = self.result.loc[9,1]
                self.t11 = self.result.loc[10,1]
                self.t12 = self.result.loc[11,1]

            #Queries to get the  lineups from the database.'''
                c.execute("SELECT full_name,position,team FROM players WHERE player_id = ANY (%s)",(self.t1,))
                self.t1_row = c.fetchall()
                c.execute("SELECT full_name,position,team FROM players WHERE player_id = ANY (%s)",(self.t2,))
                self.t2_row = c.fetchall()
                c.execute("SELECT full_name,position,team FROM players WHERE player_id = ANY (%s)",(self.t3,))
                self.t3_row = c.fetchall()
                c.execute("SELECT full_name,position,team FROM players WHERE player_id = ANY (%s)",(self.t4,))
                self.t4_row = c.fetchall()
                c.execute("SELECT full_name,position,team FROM players WHERE player_id = ANY (%s)",(self.t5,))
                self.t5_row = c.fetchall() 
                c.execute("SELECT full_name,position,team FROM players WHERE player_id = ANY (%s)",(self.t6,))
                self.t6_row = c.fetchall()
                c.execute("SELECT full_name,position,team FROM players WHERE player_id = ANY (%s)",(self.t7,))
                self.t7_row = c.fetchall()
                c.execute("SELECT full_name,position,team FROM players WHERE player_id = ANY (%s)",(self.t8,))
                self.t8_row = c.fetchall()
                c.execute("SELECT full_name,position,team FROM players WHERE player_id = ANY (%s)",(self.t9,))
                self.t9_row = c.fetchall()
                c.execute("SELECT full_name,position,team FROM players WHERE player_id = ANY (%s)",(self.t10,))
                self.t10_row = c.fetchall()
                c.execute("SELECT full_name,position,team FROM players WHERE player_id = ANY (%s)",(self.t11,))
                self.t11_row = c.fetchall()
                c.execute("SELECT full_name,position,team FROM players WHERE player_id = ANY (%s)",(self.t12,))
                self.t12_row = c.fetchall()
            #taking results from database and putting them in a dictionary.
                self.team_rows = [self.t1_row,
                        self.t2_row,
                        self.t3_row,
                        self.t4_row,
                        self.t5_row,
                        self.t6_row,
                        self.t7_row,
                        self.t8_row,
                        self.t9_row,
                        self.t10_row,
                        self.t11_row,
                        self.t12_row]
            #Putting dictionary into dataframe
                self.df_team = pd.DataFrame.from_dict(self.team_rows)
            #Transposing the table for better table management
                self.team_results = self.df_team.transpose()
            #preparing the table data for the table
                self.table_data1 = "```" +  tabulate(self.team_results[0], headers=[], showindex=False, tablefmt='plain')+ "```"
                self.table_data2 = "```" +  tabulate(self.team_results[1], headers=[], showindex=False, tablefmt='plain')+ "```"
                self.table_data3 = "```" +  tabulate(self.team_results[2], headers=[], showindex=False, tablefmt='plain')+ "```"
                self.table_data4 = "```" +  tabulate(self.team_results[3], headers=[], showindex=False, tablefmt='plain')+ "```"
                self.table_data5 = "```" +  tabulate(self.team_results[4], headers=[], showindex=False, tablefmt='plain')+ "```"
                self.table_data6 = "```" +  tabulate(self.team_results[5], headers=[], showindex=False, tablefmt='plain')+ "```"
                self.table_data7 = "```" +  tabulate(self.team_results[6], headers=[], showindex=False, tablefmt='plain')+ "```"
                self.table_data8 = "```" +  tabulate(self.team_results[7], headers=[], showindex=False, tablefmt='plain')+ "```"
                self.table_data9 = "```" +  tabulate(self.team_results[8], headers=[], showindex=False, tablefmt='plain')+ "```"
                self.table_data10 = "```" +  tabulate(self.team_results[9], headers=[], showindex=False, tablefmt='plain')+ "```"
                self.table_data11 = "```" +  tabulate(self.team_results[10], headers=[], showindex=False, tablefmt='plain')+ "```"
                self.table_data12 = "```" +  tabulate(self.team_results[11], headers=[],showindex=False, tablefmt='plain')+ "```"
            #Stripping the data of non essiental characters 
                self.table1 = str(re.sub(r"[),[('']", '', str(self.table_data1)))
                self.table2 = str(re.sub(r"[),[('']", '', str(self.table_data2)))
                self.table3 = str(re.sub(r"[),[('']", '', str(self.table_data3)))
                self.table4 = str(re.sub(r"[),[('']", '', str(self.table_data4)))
                self.table5 = str(re.sub(r"[),[('']", '', str(self.table_data5)))
                self.table6 = str(re.sub(r"[),[('']", '', str(self.table_data6)))
                self.table7 = str(re.sub(r"[),[('']", '', str(self.table_data7)))
                self.table8 = str(re.sub(r"[),[('']", '', str(self.table_data8)))
                self.table9 = str(re.sub(r"[),[('']", '', str(self.table_data9)))
                self.table10 = str(re.sub(r"[),[('']", '', str(self.table_data10)))
                self.table11 = str(re.sub(r"[),[('']", '', str(self.table_data11)))
                self.table12 = str(re.sub(r"[),[('']", '', str(self.table_data12)))
            #preparing the embed to be sent.
                self.embed = discord.Embed(title=self.league_name['name'] + ' ' + 'Lineups' + ' ' + 'Week' + ' ' + self.week, colour=5763719)
                self.embed.add_field(name=self.p1, value=self.table1, inline=False)
                self.embed.add_field(name=self.p2, value=self.table2, inline=False)
                self.embed.add_field(name=self.p3, value=self.table3, inline=False)
                self.embed.add_field(name=self.p4, value=self.table4, inline=False)
                self.embed.add_field(name=self.p5, value=self.table5, inline=False)
                self.embed.add_field(name=self.p6, value=self.table6, inline=False)
                self.embed.add_field(name=self.p7, value=self.table7, inline=False)
                self.embed.add_field(name=self.p8, value=self.table8, inline=False)
                self.embed.add_field(name=self.p9, value=self.table9, inline=False)
                self.embed.add_field(name=self.p10, value=self.table10, inline=False)
                self.embed.add_field(name=self.p11, value=self.table11, inline=False)
                self.embed.add_field(name=self.p12, value=self.table12, inline=False)
                await interaction.response.defer()
                await interaction.followup.send(embed=self.embed)

        except Exception:
            connection.rollback()
            await interaction.response.send_message('Whoops something went wrong')

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Lineups(bot), guilds=[discord.Object(id=GUILD)])
