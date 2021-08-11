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
    async def get_lineups(self,ctx,arg):
        c.execute("SELECT league_number FROM league WHERE league_name = %s;",(arg,))
        rows = c.fetchall()
        if len(rows) == 0: #if none found, return error
            await ctx.send('No league found.')
        else:
            self.results str(re.sub(r'[]),[(]', '', str(rows))) #stripping results of query so it can be passed to the table
            self.league = League(self.results)
            self.league_name = self.league.get_league()
            self.rosters = self.league.get_rosters()
            self.users = self.league.get_users()
            #getting the user display names, based on roster ID * never changes once league is set up
            self.df_users = pd.DataFrame.from_dict(users)
            self.usernames = self.df_users['display_name']
            #getting the starting lineups to query the database
            self.df_players = pd.DataFrame.from_dict(rosters)
            self.starters = self.df_players['starters']
            #preparing the query to send to the database
            c.execute

def setup(client):#setting up the disocrd client, must have this for COGS to work!
    client.add_cog(Lineups(client))
