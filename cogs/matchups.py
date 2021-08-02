import discord 
from discord.ext import commands
from sleeper_wrapper import League
import pandas as pd
from tabulate import tabulate
from db_connect import connection
import re
c = connection.cursor()



class Matchups(commands.Cog):

    def __init__(self,client):
        self.client = client


    @commands.command(name='matchups', help='Get matchups and scores for the requested league')
    async def get_matchups(self,ctx,arg1,arg2):
        c.execute("SELECT league_number FROM league WHERE league_name = %s;",(arg1,))
        rows = c.fetchall()
        if len(rows) == 0: #if none found, return error
            await ctx.send('No league found.')
        else:
            self.results = str(re.sub(r'[]),[(]', '', str(rows))) #stripping results of query so it can be passed to the table
            self.league = League(self.results)
            self.week = arg2
            self.league_name = self.league.get_league()
            self.rosters = self.league.get_rosters()
            self.users = self.league.get_users()
            self.matchups = self.league.get_matchups(self.week)
            self.scoreboards = self.league.get_scoreboards(self.rosters,self.matchups,self.users,self.week)
            self.df = pd.DataFrame.from_dict(self.scoreboards)
            self.df[self.df.columns[[0,1,2,3]]]
            self.transpose_df = self.df.transpose()
            self.table_data = tabulate(self.transpose_df, headers=['Team 1','Team 2'], showindex=False, tablefmt='plain')
            self.table = str(re.sub(r"[),[('']", '', str(self.table_data)))
            self.embed = discord.Embed(title=self.league_name['name'] + ' ' + 'Week' + ' ' + self.week + ' ' +  'Matchup', description=self.table, colour=5793266) #setting up the table to be embeded

            await ctx.send(embed=self.embed)

def setup(client):#setting up the disocrd client, must have this for COGS to work!
    client.add_cog(Matchups(client))
