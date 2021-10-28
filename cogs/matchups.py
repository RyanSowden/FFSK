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
            self.results = str(re.sub(r"[]),[('']", '', str(rows))) #stripping results of query so it can be passed to the table
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

            '''
            To make sure the matchups display correctly inside discord, each table result needs to be returned as an individual result and made into a seperate table
            '''
            self.table_data1 = "```" +  tabulate(self.df[1], headers=[], showindex=False, tablefmt='plain')+ "```"
            self.table_data2 = "```" +  tabulate(self.df[2], headers=[], showindex=False, tablefmt='plain')+ "```"
            self.table_data3 = "```" +  tabulate(self.df[3], headers=[], showindex=False, tablefmt='plain')+ "```"
            self.table_data4 = "```" +  tabulate(self.df[4], headers=[], showindex=False, tablefmt='plain')+ "```"
            self.table_data5 = "```" +  tabulate(self.df[5], headers=[], showindex=False, tablefmt='plain')+ "```"
            self.table_data6 = "```" +  tabulate(self.df[6], headers=[], showindex=False, tablefmt='plain')+ "```"
            self.table1 = str(re.sub(r"[),[('']", '', str(self.table_data1)))
            self.table2 = str(re.sub(r"[),[('']", '', str(self.table_data2)))
            self.table3 = str(re.sub(r"[),[('']", '', str(self.table_data3)))
            self.table4 = str(re.sub(r"[),[('']", '', str(self.table_data4)))
            self.table5 = str(re.sub(r"[),[('']", '', str(self.table_data5)))
            self.table6 = str(re.sub(r"[),[('']", '', str(self.table_data6)))
            #self.embed = discord.Embed(title=self.league_name['name'] + ' ' + 'Week' + ' ' + self.week + ' ' +  'Matchup', description=self.table, colour=5793266) #setting up the table to be embeded
            self.embed = discord.Embed(title=self.league_name['name'] + ' ' + 'Matchups' + ' ' + 'Week' + ' ' + self.week, colour=15548997)
            self.embed.add_field(name='1', value=self.table1, inline=False)
            self.embed.add_field(name='2', value=self.table2, inline=False)
            self.embed.add_field(name='3', value=self.table3, inline=False)
            self.embed.add_field(name='4', value=self.table4, inline=False)
            self.embed.add_field(name='5', value=self.table5, inline=False)
            self.embed.add_field(name='6', value=self.table6, inline=False)

            await ctx.send(embed=self.embed)

def setup(client):#setting up the disocrd client, must have this for COGS to work!
    client.add_cog(Matchups(client))
