import discord
from discord.ext import commands
from sleeper_wrapper import League
import pandas as pd
from tabulate import tabulate
from db_connect import connection
import re
            
c = connection.cursor()

#function that allows user to assign leagues to names of their choice
class Assign(commands.Cog):

    def __init___(self,client):
        self.client = client

    @commands.command(name='assign', help='Assign league name to league ID')
    @commands.has_role("Admin")#Ensuring the approiate role is met, will be diffeerent for each server... must ensure user has the role to be able to use the below function
    async def assign_league(self,ctx,arg1,arg2):
        self.league_number = arg1
        self.league_name = arg2
        
        try:
            c.execute("SELECT * FROM league WHERE league_name = %s;",(self.league_name,))
            rows = c.fetchall()

            if len(rows) == 0:
                c.execute("INSERT INTO league (league_name,league_number) VALUES(%s,%s)",(self.league_name,self.league_number,))
                connection.commit()
                await ctx.send('League successfully assigned.')

            else:
                await ctx.send('League name or number already exists, please try again with a different combination.')

        except Exception:
                connection.rollback()
                await ctx.send('Whoops, something went wrong')

def setup(client): #setting up the disocrd client, must have this for COGS to work
    client.add_cog(Assign(client))


