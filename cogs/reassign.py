import discord
from discord.ext import commands
from sleeper_wrapper import League
import pandas as pd
from tabulate import tabulate
from db_connect import connection
import re
            
c = connection.cursor()

#function that allows user to reassign leagues to names of their choice
class Reassign(commands.Cog):

    def __init___(self,client):
        self.client = client

    @commands.command(name='reassign', help='reassign league name to league ID')
    @commands.has_role("Admin")#Ensuring the approiate role is met, will be diffeerent for each server... must ensure user has the role to be able to use the below function
    
    async def reassign_league(self,ctx,arg1,arg2):
        self.league_number = arg1
        self.league_name = arg2

        c.execute("SELECT * FROM league WHERE league_name = %s;",(self.league_name,))
        rows = c.fetchall()

        if len(rows) != 0:
            c.execute("UPDATE league SET league_name= %s, league_number= %s WHERE league_name= %s",(self.league_name,self.league_number,self.league_name,))
            connection.commit()
            await ctx.send('League successfully reassigned.')

        else:
            await ctx.send('League name or number does not  exist, please try again with a different combination.')

def setup(client): #setting up the disocrd client, must have this for COGS to work
    client.add_cog(Reassign(client))


    
