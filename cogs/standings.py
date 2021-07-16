import discord 
from discord.ext import commands
from sleeper_wrapper import League
from sleeper_wrapper import Players
import pandas as pd
from tabulate import tabulate




#bot command to get the standings for the requested league, will work for any sleeper league as logn as you have the league ID.

class Standings(commands.Cog):

    def __init__(self,client):
        self.client = client


    @commands.command(name='standings', help='This gets standings for the requested league')
    async def get_standings(self,ctx,arg):
        self.league = League(arg)
        self.league_name = self.league.get_league()
        self.rosters = self.league.get_rosters()
        self.users = self.league.get_users()
        self.standings = self.league.get_standings(self.rosters,self.users)
        self.df = pd.DataFrame.from_dict(self.standings)
        self.df.index = self.df.index + 1
        self.results = (self.df[self.df.columns[[0,1,2]]])
        self.results['W/L']=self.results[1] + '-'+ self.results[2]
        self.table_data = self.results.drop([1,2], axis=1)
        self.table = "```" + tabulate(self.table_data, headers=['Name','W/L'], showindex=False, tablefmt='plain') + "```"    
        self.embed = discord.Embed(title=self.league_name['name'] + ' ' + 'Standings', description=self.table, colour=5793266)
        await ctx.send(embed=self.embed)

def setup(client):
    client.add_cog(Standings(client))



