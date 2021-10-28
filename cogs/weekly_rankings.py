import discord 
from discord.ext import commands
from sleeper_wrapper import League
import pandas as pd
from tabulate import tabulate
from db_connect import connection
import re
c = connection.cursor()


class Rankings(commands.Cog):

    def __init__(self,client):
        self.client = client


    @commands.command(name='rankings', help='Get matchups and scores for the requested league')
    async def get_matchups(self,ctx):
        c.execute("SELECT league_number FROM league WHERE league_name = 'orange';",)
        orange_rows = c.fetchall()
        c.execute("SELECT league_number FROM league WHERE league_name = 'yellow';",)
        yellow_rows = c.fetchall()
        c.execute("SELECT league_number FROM league WHERE league_name = 'white';",)
        white_rows = c.fetchall()
        orange_results = str(re.sub(r"[]),[('']", '', str(orange_rows))) #stripping results of query so it can be passed to the table
        yellow_results = str(re.sub(r"[]),[('']", '', str(yellow_rows))) #stripping results of query so it can be passed to the table
        white_results = str(re.sub(r"[]),[('']", '', str(white_rows))) #stripping results of query so it can be passed to the table
        db = [orange_results,white_results,yellow_results]
        if len(orange_results) == 0: #if none found, return error
            await ctx.send('No league found.')

        else:
            await ctx.send(db)



def setup(client):#setting up the disocrd client, must have this for COGS to work!
    client.add_cog(Rankings(client))
