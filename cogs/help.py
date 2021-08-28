import discord 
from discord.ext import commands
from sleeper_wrapper import League
import pandas as pd
from tabulate import tabulate
from db_connect import connection
import re



class Help(commands.Cog):

    def __init__(self,client):
        self.client = client


    @commands.command(name='help')
    async def get_help(self,ctx):
            self.embed = discord.Embed(title='Command List', colour=5793266)
            self.embed.add_field(name=';assign', value='Assign a team name to a League ID,takes 2 arguments(league,#)(*must have sufficient role).', inline=False)
            self.embed.add_field(name=';reassign', value='Reassign a team name ot a new League ID, takes 2 arguments(league,#)(*must have sufficient role).', inline=False)
            self.embed.add_field(name=';lineups', value='Gets the current starting lineups for given league, takes 2 arguments(league,week)', inline=False)
            self.embed.add_field(name=';matchups', value='Gets the current matchups for given league, takes 2 arguments(league,week)', inline=False)
            self.embed.add_field(name=';standings', value='Gets the current standings for given league, takes 1 argument(league)', inline=False)

            await ctx.send(embed=self.embed)

def setup(client):#setting up the disocrd client, must have this for COGS to work!
    client.add_cog(Help(client))
