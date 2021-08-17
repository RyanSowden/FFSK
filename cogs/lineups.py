import discord 
from discord.ext import commands
from sleeper_wrapper import League
import pandas as pd
from tabulate import tabulate
from db_connect import connection
import re

c = connection.cursor()

#bot command to get the starting lineups for all palers in the requested league.
class Lineups(commands.Cog):

    def __init__(self,client):
        self.client = client


    @commands.command(name='lineups', help='Get starting lineups for the requested league')
    async def get_lineups(self,ctx,arg1,arg2):
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
            self.lineups = self.league.get_lineups(self.rosters,self.matchups,self.users,self.week)
            self.df = pd.DataFrame.from_dict(self.lineups)
            self.result = self.df.transpose()
            '''Below fetches the usernames in the league, which is used for the table headings.'''
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
            '''Below fetches the teams to be sent to the database'''
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

            c.execute("SELECT * FROM players WHERE player_id = ANY (%s)",(self.t2,))
            self.rows = c.fetchall()
            await ctx.send(self.rows)
def setup(client):#setting up the disocrd client, must have this for COGS to work!
    client.add_cog(Lineups(client))
