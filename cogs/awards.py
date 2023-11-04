
import discord 
import os
from discord.ext import commands
from discord import app_commands
from sleeper_wrapper import League
import pandas as pd
from tabulate import tabulate
from db_connect import connection
import re
from sqlalchemy import create_engine

GUILD = os.getenv('GUILD_ID')
c = connection.cursor()

engine = create_engine('postgresql+psycopg2://{user}:{pw}@localhost/{db}'
                                       .format(user='test',
                                               pw='test',
                                               db='ffsk'))


class Awards(commands.Cog):

    def __init__(self,bot:commands.Bot) -> None:
        self.bot = bot


    @app_commands.command(name='awards')
    async def get_matchups(self,interaction: discord.Interaction, league: str, week:str) -> None:
        """Weekly awards for selected leagues"""
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
                self.standings = self.league.get_standings(self.rosters,self.users)
                self.standings_df = pd.DataFrame.from_dict(self.standings)
                self.standings_df['league'] = self.league_name['name']
                self.results = (self.standings_df[self.standings_df.columns[[0,1,2,3,4,5]]])
                self.results['W/L']=self.results[1] + '-'+ self.results[2]#adding the 'W/L' ratio
                self.table_data = self.results.drop([1,2], axis=1)
                self.table_data.columns = ['name','pf','pa','league','w/l']
                #print(self.scoreboards[1][1][0])

                self.table_data.to_sql('standings',con=engine, if_exists = 'replace')
                
                print('Completed') 
                '''
                self.embed = discord.Embed(title=self.league_name['name'] + ' ' + 'Matchups' + ' ' + 'Week' + ' ' + self.week,colour=15548997)
            
                self.embed.add_field(name='1', value=self.table1, inline=False)
                self.embed.add_field(name='2', value=self.table2, inline=False)
                self.embed.add_field(name='3', value=self.table3, inline=False)
                self.embed.add_field(name='4', value=self.table4, inline=False)
                self.embed.add_field(name='5', value=self.table5, inline=False)
                self.embed.add_field(name='6', value=self.table6, inline=False)
                await interaction.response.defer()
                await interaction.followup.send(embed=self.embed)
                '''
        except Exception as e:
            connection.rollback()
            print(e) #logging the error to the server.
            await interaction.response.send_message("Whoops, something went wrong")

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Awards(bot), guilds=[discord.Object(id=GUILD)])
