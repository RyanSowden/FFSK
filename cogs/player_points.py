import discord 
from discord.ext import commands
from sleeper_wrapper import League
from sleeper_wrapper import Stats
import pandas as pd
from tabulate import tabulate
from db_connect import connection
import re
c = connection.cursor()

stats = Stats() #declearing the stats variable from sleeper wrapper

#bot command to get the starting lineups for all palers in the requested league.
class PlayerPoints(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.command(name='points', help='Get starting lineups for the requested league')
    async def get_player_points(self,ctx,*arg1):
        player = arg1
        player_results = str(re.sub(r"[]),[('']", '', str(player))) #stripping results of query so it can be passed to the table
        print(player_results)
        c.execute("SELECT player_id FROM players WHERE full_name = %s;",(player_results,))
        rows = c.fetchall()
        if len(rows) == 0: #if none found, return error
            await ctx.send('No league found.')
        else:
            await ctx.send(rows,week)


        #stats_week = stats.get_week_stats('regular','2021', week)
        #score = stats.get_player_week_score(stats_week,'536')

def setup(client):#setting up the disocrd client, must have this for COGS to work!
    client.add_cog(PlayerPoints(client))
